import { Button, Modal, ModalBody, ModalContent, useDisclosure } from "@heroui/react";
import axios from "axios";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import CampaignsNew from "../components/Campaigns/CampaignsNew";
import CampaignsTable from "../components/Campaigns/CampaignsTable";
import Loader from "../components/common/Loader";
import type { ICampaign } from "../types";

const CampaignsView = () => {
  const navigate = useNavigate();  
  const [campaigns, setCampaigns] = useState<ICampaign[] | null>(null);  
  const [loading, setLoading] = useState(true);
  const {isOpen, onOpen, onOpenChange} = useDisclosure();  

  useEffect(() => {
    const fetchCampaigns = async () => {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/v1/campaigns`);
        setCampaigns(response?.data?.data);
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      } catch (error: any) {
        if (error?.response?.status === 401) navigate("/auth/signin");
        console.error(error);
      } finally {
        setLoading(false);
      }
    }

    fetchCampaigns();
  }, [navigate]);

  return (
    <>
      <div className="flex flex-col gap-4 p-4 max-w-7xl mx-auto min-w-[1050px]">
        <div className="w-full flex justify-left items-center px-4 py-2">
          <h1 className="text-[40px] w-fit mr-auto">Campaigns</h1>
          <Button color="warning" onPress={onOpen}>New</Button>
        </div>
        {loading && <Loader />}
        {campaigns && (
          <CampaignsTable campaigns={campaigns} />
        )}
      </div>
      <Modal className="bg-zinc-800" isOpen={isOpen} onOpenChange={onOpenChange} size="5xl" scrollBehavior='outside'>
          <ModalContent className="p-2 sm:p-4">
              <ModalBody>
                  <div className="h-full flex items-center gap-2">
                      <span className="text-[18px] sm:text-[24px] font-[500]">Load a New Campaign</span>
                  </div>
                  <div className="w-full h-full flex grow justify-center items-center p-4 sm:p-[40px] border-[1px] border-blue-100 rounded-[9px] sm:rounded-[12px]">
                      <CampaignsNew onOpenChange={onOpenChange} />
                  </div>
              </ModalBody>
          </ModalContent>
      </Modal>
    </>
  )
}

export default CampaignsView