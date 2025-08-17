namespace JobSite.Models
{
    public class Job
    {
        public string? Id { get; set; } = "";
        public string? Url { get; set; }
        public string? Title { get; set; }
        public string? Description { get; set; }
        public string? Requirements { get; set; }
        public string? Contact { get; set; }
        public string? Phone { get; set; }
        public string? Email { get; set; }
        public string? Company { get; set; }
        public string? Location { get; set; }
        public string? PostedOn { get; set; }
        public string? Hours { get; set; }
        public string? Wage { get; set; }
        public string? Start { get; set; }
        public string? Duration { get; set; }
        public string? Apply { get; set; }
        public string? Deadline { get; set; }
        public string? Comments { get; set; }

        public void FromDict(Dictionary<string, object> dict)
        {
            Id = dict.TryGetValue("id", out object? id) && id != null ? id.ToString() : string.Empty;
            Title = dict.TryGetValue("title", out object? title) && title != null ? title.ToString() : null;
            Description = dict.TryGetValue("description", out object? description) && description != null ? description.ToString() : null;
            Requirements = dict.TryGetValue("requirements", out object? requirements) && requirements != null ? requirements.ToString() : null;
            Contact = dict.TryGetValue("contact", out object? contact) && contact != null ? contact.ToString() : null;
            Phone = dict.TryGetValue("phone", out object? phone) && phone != null ? phone.ToString() : null;
            Email = dict.TryGetValue("email", out object? email) && email != null ? email.ToString() : null;
            Company = dict.TryGetValue("company", out object? company) && company != null ? company.ToString() : null;
            Location = dict.TryGetValue("location", out object? location) && location != null ? location.ToString() : null;
            PostedOn = dict.TryGetValue("posted_on", out object? posted_on) && posted_on != null ? posted_on.ToString() : null;
            Hours = dict.TryGetValue("hours", out object? hours) && hours != null ? hours.ToString() : null;
            Wage = dict.TryGetValue("wage", out object? wage) && wage != null ? wage.ToString() : null;
            Start = dict.TryGetValue("start", out object? start) && start != null ? start.ToString() : null;
            Duration = dict.TryGetValue("duration", out object? duration) && duration != null ? duration.ToString() : null;
            Apply = dict.TryGetValue("apply", out object? apply) && apply != null ? apply.ToString() : null;
            Deadline = dict.TryGetValue("deadline", out object? deadline) && deadline != null ? deadline.ToString() : null;
            Comments = dict.TryGetValue("comments", out object? comments) && comments != null ? comments.ToString() : null;
        }
    }
}
