import { NextResponse } from 'next/server'

export async function GET(request: Request) {
    try {
        const { searchParams } = new URL(request.url)
        const table = searchParams.get('table') || 'car_data'
        console.log(`Fetching data for table: ${table}`)

        const response = await fetch(`http://127.0.0.1:8000/latest/${table}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`)
        }

        const data = await response.json()
        console.log(`Fetched data: ${JSON.stringify(data)}`)
        return NextResponse.json(data)

    } catch (error) {
        console.error('Error fetching data:', error)
        return NextResponse.json(
            { error: 'Failed to fetch data' },
            { status: 500 }
        )
    }
}
