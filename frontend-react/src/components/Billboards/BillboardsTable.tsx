import { addToast, Button, Modal, ModalBody, ModalContent, Pagination, Table, TableBody, TableCell, TableColumn, TableHeader, TableRow, Tooltip, useDisclosure } from '@heroui/react';
import axios from 'axios';
import { useCallback, useMemo, useState, type ReactNode } from 'react';
import { FiArrowUpRight } from 'react-icons/fi';
import { IoIosRemoveCircle, IoMdAddCircle } from "react-icons/io";
import { MdDelete } from 'react-icons/md';
import { useNavigate } from 'react-router-dom';
import type { IBillboard, ILocation } from '../../types';
import ItemsMap from '../common/ItemsMap';
import BillboardsNewEdit from './BillboardsNewEdit';

interface IProps {
    billboards: IBillboard[];
    current?: boolean;
    available?: boolean;
}

const BillboardsTable = ({ billboards, current, available }: IProps) => {
    const navigate = useNavigate();
    const [loadingAction, setLoadingAction] = useState(false);
    const {isOpen, onOpen, onOpenChange} = useDisclosure();
    const [billboardToEdit, setBillboardToEdit] = useState<IBillboard | null>(null);

    const openEditBillboard = useCallback((billboardEdit: IBillboard) => {
        setBillboardToEdit(billboardEdit);
        onOpen();
    }, [onOpen]);

    const columns = useMemo(() => ([
        {name: "Address", uid: "location"},
        {name: "Width", uid: "width_mt"},
        {name: "Height", uid: "height_mt"},
        {name: "Price per Day", uid: "dollars_per_day"},
        {name: "", uid: "actions"},
    ]), []);

    const billboardItems = useMemo(() => 
        !billboards ? [] 
        : billboards
    , [billboards]);

    const [page, setPage] = useState(1);
    const rowsPerPage = 5;
    
    const pages = Math.ceil(billboardItems.length / rowsPerPage);
    
    const items = useMemo(() => {
        const start = (page - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        return billboardItems.slice(start, end);
    }, [page, billboardItems]);

    const addBillboard = useCallback(async (addUrl: string) => {
        setLoadingAction(true);
        try {
            await axios.post(`${import.meta.env.VITE_API_URL}${addUrl}`)
            window.location.reload();
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        } catch (error: any) {
            if (error?.response?.status === 401) navigate("/auth/signin");
            addToast({ title: "Error", description: "Failed to add billboard to campaign" });
        } finally {
            setLoadingAction(false);
        }
    }, [navigate, setLoadingAction]);
    
    const removeBillboard = useCallback(async (removeUrl: string) => {
        setLoadingAction(true);
        try {
            await axios.post(`${import.meta.env.VITE_API_URL}${removeUrl}`)
            window.location.reload();
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        } catch (error: any) {
            if (error?.response?.status === 401) navigate("/auth/signin");
            addToast({ title: "Error", description: "Failed to add billboard to campaign" });
        } finally {
            setLoadingAction(false);
        }
    }, [navigate, setLoadingAction]);

    const onDeleteBillboard = useCallback(async (billboardId: string) => {
        try {
            await axios.delete(`${import.meta.env.VITE_API_URL}/api/v1/billboards/${billboardId}`);
            addToast({ title: "Success!", description: "Billboard deleted successfully." });
            window.location.reload();
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        } catch (error) {
            addToast({ title: "Error", description: "Oops, something went wrong" });
        }
    }, [])

    const renderCell = useCallback((billboard: IBillboard, columnKey: keyof IBillboard) => {
        const cellValue = billboard[columnKey];
        switch (columnKey) {
            case "location":
                return (
                    <div className="flex">
                        <p className="text-bold text-sm mx-auto">
                            {(cellValue as ILocation)?.address}, 
                            {" "}{(cellValue as ILocation)?.city}, 
                            {" "}{(cellValue as ILocation)?.state} 
                            {" ("}{(cellValue as ILocation)?.country_code}{")"}
                        </p>
                    </div>
                );
            case "width_mt":
                return (
                    <div className="flex flex-col">
                        <p>{typeof cellValue === 'string' || typeof cellValue === 'number' ? Number(cellValue).toFixed(2) : ''} mt</p>
                    </div>
                );
            case "height_mt":
                return (
                    <div className="flex flex-col">
                        <p>{typeof cellValue === 'string' || typeof cellValue === 'number' ? Number(cellValue).toFixed(2) : ''} mt</p>
                    </div>
                );
            case "dollars_per_day":
                return (
                    <div className="flex flex-col">
                        <p>$ {typeof cellValue === 'string' || typeof cellValue === 'number' ? Number(cellValue).toFixed(2) : ''}</p>
                    </div>
                );
            case "actions" as keyof IBillboard:
                return (
                    <div className="flex items-center gap-2 justify-end">
                        { (!current && !available) && (
                            <Tooltip content="Edit Billboard" showArrow={true}>
                                <Button isIconOnly variant="light" color="primary"
                                    isLoading={loadingAction}
                                    disabled={loadingAction} 
                                    onPress={() => openEditBillboard(billboard)} 
                                    className="rounded-[6px] !h-[32px] !max-w-[32px] !px-0 py-1"
                                >
                                    <FiArrowUpRight size={18} color="#2F6BDC"/>
                                </Button>
                            </Tooltip>
                        )}
                        { available && (
                            <Tooltip content="Add To Campaign" showArrow={true}>
                                <Button isIconOnly variant="light" color="success" 
                                    isLoading={loadingAction}
                                    disabled={loadingAction}
                                    onPress={() => addBillboard(billboard?.links?.actions?.find(action => action.name === "add_to_campaign")?.href || "")} 
                                    className="rounded-[6px] !h-[32px] !max-w-[32px] !px-0 py-1"
                                >
                                    <IoMdAddCircle size={24} color="rgba(74,214,43,0.9)"/>
                                </Button>
                            </Tooltip>
                        )}
                        { current && (
                            <Tooltip content="Remove From Campaign" showArrow={true}>
                                <Button isIconOnly variant="light" color="success" 
                                    isLoading={loadingAction}
                                    disabled={loadingAction}
                                    onPress={() => removeBillboard(billboard?.links?.actions?.find(action => action.name === "remove_from_campaign")?.href || "")} 
                                    className="rounded-[6px] !h-[32px] !max-w-[32px] !px-0 py-1"
                                >
                                    <IoIosRemoveCircle size={24} color="rgba(214,43,66,0.9)"/>
                                </Button>
                            </Tooltip>
                        )}
                        { (!current && !available) && (
                            <Tooltip content="Delete Billboard" showArrow={true}>
                                <Button isIconOnly variant="light" color="danger" 
                                    onPress={() => onDeleteBillboard(billboard?.id)} 
                                    className="rounded-[6px] !h-[32px] !max-w-[32px] !px-0 py-1"
                                >
                                    <MdDelete size={18} color="rgba(255,255,255,0.9)"/>
                                </Button>
                            </Tooltip>
                        )}
                    </div>
                );
            default:
                return cellValue;
        }
    }, [loadingAction, addBillboard, removeBillboard, available, current, openEditBillboard, onDeleteBillboard]);

    return (
        <>
            <div className="w-full h-full flex flex-col gap-4">

                <Table 
                    aria-label="Billboards table"
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
                                    {renderCell(item, columnKey as keyof IBillboard) as ReactNode}
                                </TableCell>
                            )}
                        </TableRow>
                    )}
                    </TableBody>
                </Table>
                <ItemsMap items={items.map(i => i?.location)} />
            </div>
            <Modal className="bg-zinc-800 z-[1000]" isOpen={isOpen} onOpenChange={onOpenChange} size="5xl" scrollBehavior='outside'>
                <ModalContent className="p-2 sm:p-4">
                    <ModalBody>
                        <div className="h-full flex items-center gap-2">
                            <span className="text-[18px] sm:text-[24px] font-[500]">Edit Location</span>
                        </div>
                        <div className="w-full h-full flex grow justify-center items-center p-4 sm:p-[40px] border-[1px] border-blue-100 rounded-[9px] sm:rounded-[12px]">
                            <BillboardsNewEdit onOpenChange={onOpenChange} billboard={billboardToEdit} />
                        </div>
                    </ModalBody>
                </ModalContent>
            </Modal>
        </>
    )
}

export default BillboardsTable