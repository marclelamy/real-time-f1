import Image from "next/image";
// import useSWR from "swr";

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function Home() {
  // const { data, error, isLoading } = useSWR("/api/v1/drivers", fetcher);
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
       <h1>TrackPulse</h1>

    </main>
  );
}
