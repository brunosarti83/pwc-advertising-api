import { addToast, Button, Pagination, Table, TableBody, TableCell, TableColumn, TableHeader, TableRow } from '@heroui/react';
import axios from 'axios';
import { useCallback, useMemo, useState, type ReactNode } from 'react';
import { FiArrowUpRight } from 'react-icons/fi';
import { IoIosRemoveCircle, IoMdAddCircle } from "react-icons/io";
import { useNavigate } from 'react-router-dom';
import type { IBillboard, ILocation } from '../../types';

interface IProps {
    billboards: IBillboard[];
    current?: boolean;
    available?: boolean;
}

const BillboardsTable = ({ billboards, current, available }: IProps) => {
    const navigate = useNavigate();
    const [loadingAction, setLoadingAction] = useState(false);

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
                        <Button isIconOnly variant="light" color="primary"
                            isLoading={loadingAction}
                            disabled={loadingAction} 
                            onPress={() => {
                                
                            }} 
                            className="rounded-[6px] !h-[32px] !max-w-[32px] !px-0 py-1"
                        >
                            <FiArrowUpRight size={18} color="#2F6BDC"/>
                        </Button>
                        { available && (
                            <Button isIconOnly variant="light" color="success" 
                                isLoading={loadingAction}
                                disabled={loadingAction}
                                onPress={() => addBillboard(billboard?.links?.actions?.find(action => action.name === "add_to_campaign")?.href || "")} 
                                className="rounded-[6px] !h-[32px] !max-w-[32px] !px-0 py-1"
                            >
                                <IoMdAddCircle size={24} color="rgba(74,214,43,0.9)"/>
                            </Button>
                        )}
                        { current && (
                            <Button isIconOnly variant="light" color="success" 
                                isLoading={loadingAction}
                                disabled={loadingAction}
                                onPress={() => removeBillboard(billboard?.links?.actions?.find(action => action.name === "remove_from_campaign")?.href || "")} 
                                className="rounded-[6px] !h-[32px] !max-w-[32px] !px-0 py-1"
                            >
                                <IoIosRemoveCircle size={24} color="rgba(214,43,66,0.9)"/>
                            </Button>
                        )}
                    </div>
                );
            default:
                return cellValue;
        }
    }, [loadingAction, addBillboard, removeBillboard, available, current]);

    return (
        <>
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
        </>
    )
}

export default BillboardsTable