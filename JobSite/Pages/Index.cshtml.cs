using FirebaseAdmin;
using Google.Cloud.Firestore;
using JobSite.Hubs;
using JobSite.Models;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.SignalR;
using System.Diagnostics;
using System.Text.Json.Nodes;

namespace JobSite.Pages
{
    public class IndexModel : PageModel
    {
        private readonly ILogger<IndexModel> _logger;

        public IndexModel(ILogger<IndexModel> logger)
        {
            _logger = logger;
        }
        static readonly string credsPath = Path.Combine("..", "creds", "credentials.json");
        static readonly string jsonString = System.IO.File.ReadAllText(credsPath);

        private readonly JsonNode? root = JsonNode.Parse(jsonString);

        public List<Job> Jobs { get; set; } = [];

        public async Task OnGetAsync()
        {
            await GetInitial();
        }

        private async Task GetInitial()
        {
            if (root == null)
            {
                _logger.LogError("Failed to parse credentials JSON.");
                return;
            }
            var projectID = (string?)root["project_id"];

            var db = FirestoreDb.Create(projectID);
            Query docQuery = db.Collection((string?)root["coll_name"]);
            QuerySnapshot docQuerySnapshot = await docQuery.GetSnapshotAsync();
            foreach (DocumentSnapshot documentSnapshot in docQuerySnapshot.Documents)
            {
                var job = new Job();
                job.FromDict(documentSnapshot.ToDictionary());
                Jobs.Add(job);
            }
        }

        public void OnCleanup()
        {
        }
    }
}
