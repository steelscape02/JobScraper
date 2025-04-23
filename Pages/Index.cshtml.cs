using JobScraper.Model;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace JobScraper.Pages;

public class IndexModel(ILogger<IndexModel> logger) : PageModel
{
    private readonly ILogger<IndexModel> _logger = logger;

    private readonly List<Job> _jobs = ListScraper.Jobs;

    public required List<Job> Jobs { get; set; }

    public void OnGet()
    {
        Jobs = _jobs;
    }

    public async Task<IActionResult> OnGetUpdateTable()
    {
        await ListScraper.Scrape();
        Jobs = ListScraper.Jobs;
        return new JsonResult(Jobs);
    }
}
