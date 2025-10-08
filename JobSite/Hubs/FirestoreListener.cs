using Google.Cloud.Firestore;
using JobSite.Models;
using JobSite.Pages;
using Microsoft.AspNetCore.SignalR;
using System.Diagnostics;
using System.Text.Json.Nodes;

namespace JobSite.Hubs
{
    public class FirestoreListener : BackgroundService
    {
        static readonly string credsPath = Path.Combine("..", "creds", "credentials.json");
        static readonly string jsonString = System.IO.File.ReadAllText(credsPath);

        FirestoreChangeListener? listener = null;

        private readonly JsonNode? root = JsonNode.Parse(jsonString);

        public List<Job> Jobs { get; set; } = [];
        private readonly IHubContext<JobHub> _hubContext;
        private readonly ILogger<IndexModel> _logger;

        public FirestoreListener(IHubContext<JobHub> hubContext, ILogger<IndexModel> logger)
        {
            _hubContext = hubContext;
            _logger = logger;
        }

        protected override Task ExecuteAsync(CancellationToken stoppingToken)
        {
            if (root == null)
            {
                _logger.LogError("Failed to parse credentials JSON.");
                throw new ArgumentNullException(nameof(root));
            }
            var projectID = (string?)root["project_id"];

            var db = FirestoreDb.Create(projectID);
            CollectionReference docRef = db.Collection((string?)root["coll_name"]);
            Debug.WriteLine(DateTimeOffset.Now.ToUnixTimeMilliseconds());
            listener = docRef.Listen(async snapshot =>
            {
                foreach (DocumentChange change in snapshot.Changes)
                {
                    switch (change.ChangeType)
                    {
                        case DocumentChange.Type.Added:
                            {

                                var job = new Job();
                                job.FromDict(change.Document.ToDictionary());
                                Jobs.Add(job);
                                await _hubContext.Clients.All.SendAsync("ReceiveAdd", job);
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
                                    await _hubContext.Clients.All.SendAsync("ReceiveUpdate", existingJob);
                                }

                                break;
                            }

                        case DocumentChange.Type.Removed:
                            {
                                var job = new Job();
                                job.FromDict(change.Document.ToDictionary());
                                await _hubContext.Clients.All.SendAsync("ReceiveRemove", job.Id);
                                Jobs.Remove(job);
                                break;
                            }
                    }
                }
            }, stoppingToken);
            return Task.CompletedTask;
        }
    }
}
