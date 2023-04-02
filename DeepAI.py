import requests

def CustomDeepImage(prompt):
    r = requests.post(
        "https://api.deepai.org/api/cyberpunk-generator",
        data={
            'text': prompt,
            'grid_size' : '1'
        },
        headers={'api-key': '0c635ab5-65c0-40b0-8204-874308c13130'}
    )
    return(r.json())
