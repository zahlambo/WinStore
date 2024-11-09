import { useEffect, useState } from "react";
import Card from "../components/Card";

interface AppData {
  id: string;
  name: string;
  icon: string;
}

function Body() {
  const backendMainURL = import.meta.env.VITE_BACKEND_MAIN_URL as string;
  const [allApps, setAllApps] = useState<AppData[]>([]);
  
  const searchData = async (params?: string) => {
    let data: AppData[] = [];
    try {
      const response = await fetch(
        params 
          ? `${backendMainURL}/get_all_items?search=${params}`
          : `${backendMainURL}/get_all_items`
      );
      data = await response.json();
      console.log("Data fetched:", data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
    setAllApps(data);
  };

  useEffect(() => {searchData();}, []);

  return (
    <div className="flex px-16 gap-8">
      {allApps.map(app => (
        <Card key={app.id} id={app.id} name={app.name} icon={app.icon.replace(/width="[^"]+"/, 'width="75%"').replace(/height="[^"]+"/, 'height="75%"')} />
      ))}
    </div>
  );
}

export default Body;
