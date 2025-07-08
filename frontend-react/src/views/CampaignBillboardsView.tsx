import axios from "axios";
import { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import BillboardsTable from "../components/Billboards/BillboardsTable";
import Loader from "../components/common/Loader";
import type { IBillboard, ICampaign } from "../types";

const CampaignBillboardsView = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();  
  const [campaign, setCampaign] = useState<ICampaign | null>(null);  
  const [availableBillboards, setAvailableBillboards] = useState<IBillboard[]>([]);  
  const [loading, setLoading] = useState(true);  

  useEffect(() => {
    const fetchCampaign = async () => {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/v1/campaigns/${id}`);
        setCampaign(response?.data?.data);
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      } catch (error: any) {
        if (error?.response?.status === 401) navigate("/auth/signin");
        console.error(error);
      } finally {
        setLoading(false);
      }
    }

    fetchCampaign();
  }, [navigate, id]);

  useEffect(() => {
    const fetchAvailable = async () => {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/v1/availability/?campaign_id=${id}`);
        setAvailableBillboards(response?.data?.data);
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      } catch (error: any) {
        if (error?.response?.status === 401) navigate("/auth/signin");
        console.error(error);
      } finally {
        setLoading(false);
      }
    }

    fetchAvailable();
  }, [navigate, id]);

  const currentBillboards = useMemo(() => campaign?.billboards, [campaign]);

  return (
    <>
      <div className="flex flex-col gap-4 p-4 max-w-7xl mx-auto min-w-[1050px]">
        <div className="w-full flex  flex-col justify-center px-4 py-2">
          <h1 className="text-[40px] w-fit mr-auto">{campaign?.name}</h1>
          <div className="w-full flex justify-between items-center">
            <span className="text-[24px]">From: {campaign?.start_date}</span>
            <span className="text-[24px]">To: {campaign?.end_date}</span>
          </div>
        </div>
        {loading && <Loader />}
        {currentBillboards && (
          <div className="w-full flex flex-col justify-center items-center px-4 py-2 gap-8">
            <div className="flex flex-col gap-4 w-full">
              <h3 className="text-[24px] w-fit mr-auto">Current Billboards in this Campaign</h3>
                <BillboardsTable billboards={currentBillboards} current />
            </div>
            <div className="flex flex-col gap-4 w-full">
              <h3 className="text-[24px] w-fit mr-auto">Available Billboards for this Campaign</h3>
                <BillboardsTable billboards={availableBillboards} />
            </div>
          </div>
        )}
      </div>
    </>
  )
}

export default CampaignBillboardsView