'use client'

import Image from "next/image";
import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then(res => res.json())

export default function Home() {
    const { data, error } = useSWR('/api?table=car_data', fetcher, {
        refreshInterval: 1
    })

    if (error) return <div>Failed to load</div>
    if (!data) return <div>Loading...</div>

    return (
        <div>
            <h1>Real-Time F1</h1>
            <pre>{JSON.stringify(data, null, 2)}</pre>
            <p>{error}</p>
        </div>
    );
}
