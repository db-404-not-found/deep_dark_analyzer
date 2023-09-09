const postEndpoint = ''
const getEndpoint = ''

export async function sendToAnalyze(text: string) {
    const response = await fetch(`${import.meta.env.VITE_API_URL}${postEndpoint}`, {
        method: 'POST',
        body: JSON.stringify(text)
    })

    if (!response.ok) {
        throw new Error('Sending text to analyze failed')
    }

    return response.json()
}

export async function fetchResult() {
    const response = await fetch(`${import.meta.env.VITE_API_URL}${getEndpoint}`, {
        method: 'GET',
    })

    if (!response.ok) {
        throw new Error('Fetching result of analyzing failed')
    }

    return response.json()
}