using FirebaseAdmin;
using Google.Cloud.Firestore;
using JobSite.Hubs;
using JobSite.Models;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.SignalR;
using System.Diagnostics;
using System.Text.Json.Nodes;
using System;
using System.IO;

namespace JobSite.Pages
{
    public class IndexModel : PageModel
    {
        private readonly ILogger<IndexModel> _logger;
        private readonly IHubContext<JobHub> _hubContext;

        public IndexModel(ILogger<IndexModel> logger, IHubContext<JobHub> hubContext)
        {
            _logger = logger;
            _hubContext = hubContext;
        }
        static readonly string credsPath = Path.Combine("..","creds", "credentials.json");
        static readonly string jsonString = System.IO.File.ReadAllText(credsPath);

        FirestoreChangeListener? listener = null;

        private readonly JsonNode? root = JsonNode.Parse(jsonString);

        public List<Job> Jobs { get; set; } = [];

        public void OnGet()
        {
            if (root == null)
            {
                _logger.LogError("Failed to parse credentials JSON.");
                return;
            }
            var projectID = (string?)root["project_id"];
            var db = FirestoreDb.Create(projectID);
            CollectionReference docRef = db.Collection((string?)root["coll_name"]);
            listener = docRef.Listen(snapshot =>
            {
                foreach (DocumentChange change in snapshot.Changes)
                {
                    switch (change.ChangeType)
                    {
                        case DocumentChange.Type.Added:
                            {
                                
                                var job = new Job();
                                job.FromDict(change.Document.ToDictionary());
                                Debug.WriteLine($"Adding job : {job.Title}");
                                Jobs.Add(job);
                                _ = _hubContext.Clients.All.SendAsync("ReceiveAdd", job);
                                break;
                            }

                        case DocumentChange.Type.Modified:
                            {
                                var job = new Job();
                                job.FromDict(change.Document.ToDictionary());
                                var existingJob = Jobs.FirstOrDefault(j => j.Url == job.Url);
                                if (existingJob != null)
                                {
                                    existingJob.FromDict(change.Document.ToDictionary());
                                    Debug.WriteLine($"Modifying job : {job.Title}");
                                    _ = _hubContext.Clients.All.SendAsync("ReceiveUpdate", existingJob);
                                }

                                break;
                            }

                        case DocumentChange.Type.Removed:
                            {
                                var job = new Job();
                                job.FromDict(change.Document.ToDictionary());
                                Jobs.Remove(job);
                                _ = _hubContext.Clients.All.SendAsync("ReceiveRemove", job.Title);
                                break;
                            }
                    }
                }
            });
        }

        public void OnCleanup()
        {
            if (listener != null)
            {
                listener.StopAsync().Wait();
                listener = null;
            }
        }
    }
}
