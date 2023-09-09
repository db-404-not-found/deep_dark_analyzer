const postEndpoint = 'api/v1/tasks'
const getEndpoint = 'api/v1/tasks'

const defaultHeaders = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

export async function sendToAnalyze(press_release: string) {
    const response = await fetch(`${import.meta.env.VITE_API_URL}${postEndpoint}`, {
        method: 'POST',
        body: JSON.stringify({press_release}),
        headers: defaultHeaders
    })

    if (!response.ok) {
        throw new Error('Sending text to analyze failed')
    }

    return response.json()
}

export async function fetchResult(id: string) {
    const response = await fetch(`${import.meta.env.VITE_API_URL}${getEndpoint}/${id}`, {
        method: 'GET',
    })

    if (!response.ok) {
        throw new Error('Fetching result of analyzing failed')
    }

    return response.json()
}