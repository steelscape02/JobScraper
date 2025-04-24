
namespace JobScraper;

public abstract class Program
{

    public static void Main(string[] args)
    {
        //await Model.ListScraper.Scrape();
        var port = Environment.GetEnvironmentVariable("PORT") ?? "8080";
        var builder = WebApplication.CreateBuilder(args);
        // Add services to the container.
        builder.Services.AddRazorPages();

        builder.WebHost.ConfigureKestrel(options =>
        {
            options.ListenAnyIP(Int32.Parse(port)); // Listen on 0.0.0.0
        });

        var app = builder.Build();

        // Configure the HTTP request pipeline.
        if (!app.Environment.IsDevelopment())
        {
            app.UseExceptionHandler("/Error");
            // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
            app.UseHsts();
        }
        
        app.UseStaticFiles();
        app.UseHttpsRedirection();

        app.UseRouting();

        app.UseAuthorization();

        //app.MapStaticAssets();
        app.MapRazorPages();
            //.WithStaticAssets();

        app.Run();
    }
}