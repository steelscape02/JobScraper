namespace JobSite.Hubs
{
    using Microsoft.AspNetCore.SignalR;
    using JobSite.Models;

    public class JobHub : Hub
    {
        public async Task Add(Job job)
        {
            await Clients.All.SendAsync("ReceiveAdd", job);
        }
        public async Task Update(Job job)
        {
            await Clients.All.SendAsync("ReceiveUpdate", job);
        }
        public async Task Remove(string url)
        {
            await Clients.All.SendAsync("ReceiveRemove", url);
        }
    }
    
}
