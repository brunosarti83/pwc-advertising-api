import { addToast, Button, Modal, ModalBody, ModalContent, Pagination, Table, TableBody, TableCell, TableColumn, TableHeader, TableRow, Tooltip, useDisclosure } from '@heroui/react';
import axios from 'axios';
import { useCallback, useMemo, useState, type ReactNode } from 'react';
import { FaSign } from 'react-icons/fa';
import { FiArrowUpRight } from 'react-icons/fi';
import { MdDelete } from "react-icons/md";
import { useNavigate } from 'react-router-dom';
import type { ICampaign } from '../../types';
import CampaignsNewEdit from './CampaignsNewEdit';

interface IProps {
    campaigns: ICampaign[]
}

const CampaignsTable = ({ campaigns }: IProps) => {
    const navigate = useNavigate();
    const {isOpen, onOpen, onOpenChange} = useDisclosure();
    const [campaignToEdit, setCampaignToEdit] = useState<ICampaign | null>(null);
    
    const openEditCampaign = useCallback((campaignEdit: ICampaign) => {
        setCampaignToEdit(campaignEdit);
        onOpen();
    }, [onOpen]);

    const onDeleteCampaign = useCallback(async (campaignId: string) => {
        try {
            await axios.delete(`${import.meta.env.VITE_API_URL}/api/v1/campaigns/${campaignId}`);
            addToast({ title: "Success!", description: "Campaign deleted successfully." });
            window.location.reload();
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        } catch (error: any) {
            if (error?.response?.status === 409) {
                addToast({ title: "Forbidden", description: "This campaign already has billboards assigned to it" });
            } else addToast({ title: "Error", description: "Oops, something went wrong" });
        }
    }, [])
    
    const columns = useMemo(() => ([
        {name: "Name", uid: "name"},
        {name: "Start", uid: "start_date"},
        {name: "End", uid: "end_date"},
        {name: "Billboards", uid: "billboards"},
        {name: "Total Cost", uid: "total_dollar_amount"},
        {name: "", uid: "actions"},
    ]), []);

    const campaignItems = useMemo(() => 
        !campaigns ? [] 
        : campaigns
    , [campaigns]);

    const [page, setPage] = useState(1);
    const rowsPerPage = 5;
    
    const pages = Math.ceil(campaignItems.length / rowsPerPage);
    
    const items = useMemo(() => {
        const start = (page - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        return campaignItems.slice(start, end);
    }, [page, campaignItems]);

    const renderCell = useCallback((campaign: ICampaign, columnKey: keyof Omit<ICampaign, "links">) => {
        const cellValue = columnKey !== "billboards" ? campaign[columnKey] : campaign[columnKey].length;
        switch (columnKey) {
            case "name":
                return (
                    <div className="flex">
                        <p className="text-bold text-sm mx-auto">
                            {cellValue}
                        </p>
                    </div>
                );
            case "start_date":
                return (
                    <div className="flex">
                        <p className="text-bold text-sm mx-auto">
                            {cellValue}
                        </p>
                    </div>
                );
            case "end_date":
                return (
                    <div className="flex">
                        <p className="text-bold text-sm mx-auto">
                            {cellValue}
                        </p>
                    </div>
                );
            case "billboards":
                return (
                    <div className="flex">
                        <p className="text-bold text-sm mx-auto">
                            {cellValue}
                        </p>
                    </div>
                );
            case "total_dollar_amount":
                return (
                    <div className="flex">
                        <p className="text-bold text-sm mx-auto">
                            {cellValue}
                        </p>
                    </div>
                );
            case "actions" as keyof ICampaign:
                return (
                    <div className="flex gap-2 items-center justify-end">
                        <Tooltip content="Edit Campaign" showArrow={true}>
                            <Button isIconOnly variant="light" color="primary" 
                                onPress={() => openEditCampaign(campaign)} 
                                className="rounded-[6px] !h-[32px] !max-w-[32px] !px-0 py-1"
                            >
                                <FiArrowUpRight size={18} color="#2F6BDC"/>
                            </Button>
                        </Tooltip>
                        <Tooltip content="Manage Campaign's Billboards" showArrow={true}>
                            <Button isIconOnly variant="light" color="success" 
                                onPress={() => {
                                navigate(`/campaign-billboards/${campaign.id}`); 
                                }} 
                                className="rounded-[6px] !h-[32px] !max-w-[32px] !px-0 py-1"
                            >
                                <FaSign size={18} color="rgba(255,255,255,0.9)"/>
                            </Button>
                        </Tooltip>
                        <Tooltip content="Delete Campaign" showArrow={true}>
                            <Button isIconOnly variant="light" color="danger" 
                                onPress={() => onDeleteCampaign(campaign?.id)} 
                                className="rounded-[6px] !h-[32px] !max-w-[32px] !px-0 py-1"
                            >
                                <MdDelete size={18} color="rgba(255,255,255,0.9)"/>
                            </Button>
                        </Tooltip>
                    </div>
                );
            default:
                return cellValue;
        }
    }, [navigate, openEditCampaign, onDeleteCampaign]);

    return (
        <>
            <Table 
                aria-label="Campaigns table"
                classNames={{
                    wrapper: "!border-blue-100 border-[1px] shadow-none user-select-none overflow-x-auto w-[1050px]",
                    tr: "border-b border-divider border-blue-100", 
                    th: "!bg-transparent border-b border-blue-100 text-[14px] text-white font-roboto font-[500] pb-4", 
                }}
                bottomContent={
                    <div className="flex w-full justify-center">
                        <Pagination
                        variant="bordered"
                        showControls
                        showShadow
                        color="primary"
                        radius="sm"
                        page={page}
                        total={pages}
                        onChange={(page) => setPage(page)}
                        classNames={{
                            base: "",
                            wrapper: "",
                            item: "rounded-[6px] border-gray-500 border-[1px] data-[active=true]:text-blue-400 data-[active=true]:border-[2px] data-[active=true]:border-blue-400",
                            cursor: "bg-transparent text-blue-400 font-bold border-[1px] border-blue-400",
                        }}
                        />
                    </div>
                }
            >
                <TableHeader columns={columns}>
                {(column) => (
                    <TableColumn key={column.uid} align={"center"}>
                        {column.name}
                    </TableColumn>
                )}
                </TableHeader>
                <TableBody items={items}>
                {(item) => (
                    <TableRow key={item.id}>
                        {(columnKey) => (
                            <TableCell className="">
                                {renderCell(item, columnKey as keyof Omit<ICampaign, "links">) as ReactNode}
                            </TableCell>
                        )}
                    </TableRow>
                )}
                </TableBody>
            </Table>
            <Modal className="bg-zinc-800 z-[1000]" isOpen={isOpen} onOpenChange={onOpenChange} size="5xl" scrollBehavior='outside'>
                <ModalContent className="p-2 sm:p-4">
                    <ModalBody>
                        <div className="h-full flex items-center gap-2">
                            <span className="text-[18px] sm:text-[24px] font-[500]">Edit Location</span>
                        </div>
                        <div className="w-full h-full flex grow justify-center items-center p-4 sm:p-[40px] border-[1px] border-blue-100 rounded-[9px] sm:rounded-[12px]">
                            <CampaignsNewEdit onOpenChange={onOpenChange} campaign={campaignToEdit} />
                        </div>
                    </ModalBody>
                </ModalContent>
            </Modal>
        </>
    )
}

export default CampaignsTable