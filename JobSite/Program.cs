using JobSite.Hubs;
var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddRazorPages();
builder.Services.AddSignalR(options =>
{
    options.ClientTimeoutInterval = TimeSpan.FromSeconds(120);
    options.KeepAliveInterval = TimeSpan.FromSeconds(100);
    
});
builder.Services.AddHsts(options =>
{
    //options.Preload = true; //Do not enable until MaxAge is set to 1 yr and valid cert is present
    options.IncludeSubDomains = true;
    options.MaxAge = TimeSpan.FromMinutes(5); //TODO: ramp from 5 min to 1 week, to 1 month, etc
});

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    app.UseHsts(); // HTTP Strict Transport Security
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

app.UseAuthorization();

app.MapRazorPages();
app.MapHub<JobHub>("/jobHub");

app.Run();
