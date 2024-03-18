from apify_client import ApifyClient

YOUR_API_KEY = "YOUR_API_KEY"  # Replace with your API key
CATEGORY_URL = "https://www.udemy.com/courses/development/python/"  # Replace with the category URL


# Create the ApifyClient instance

apify_client = ApifyClient(YOUR_API_KEY)

# Prepare the Actor input
run_input = {
    "category_url": [{"url": CATEGORY_URL}],
    "max_items": 15000,
    "start_page": 1,
    "proxySettings": {
        "useApifyProxy": True,
        "apifyProxyGroups": ["BUYPROXIES94952"],
        "apifyProxyCountry": "US",
    },
}

# Run the Actor and wait for it to finish
# The acotor used for this scrapping has this id: 0qtntHCmAJ1Fbw8AK
run = apify_client.actor("0qtntHCmAJ1Fbw8AK").call(run_input=run_input)
