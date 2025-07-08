import { Button, Pagination, Table, TableBody, TableCell, TableColumn, TableHeader, TableRow } from '@heroui/react';
import { useCallback, useMemo, useState, type ReactNode } from 'react';
import { FiArrowUpRight } from 'react-icons/fi';
import type { IBillboard, ILocation } from '../../types';

interface IProps {
    billboards: IBillboard[]
}

const BillboardsTable = ({ billboards }: IProps) => {

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

    const renderCell = useCallback((billboard: IBillboard, columnKey: keyof IBillboard) => {
        const cellValue = billboard[columnKey];
        switch (columnKey) {
            case "location":
                return (
                    <div className="flex">
                        <p className="text-bold text-sm">
                            {(cellValue as ILocation)?.address}, 
                            {(cellValue as ILocation)?.city}, 
                            {(cellValue as ILocation)?.state} 
                            {"("}{(cellValue as ILocation)?.country_code}{")"}
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
                    <div className="flex flex-col items-center">
                        <Button isIconOnly variant="light" color="primary" 
                            onPress={() => {
                                
                            }} 
                            className="rounded-[6px] !h-[32px] !max-w-[32px] !px-0 py-1"
                        >
                            <FiArrowUpRight size={18} color="#2F6BDC"/>
                        </Button>
                    </div>
                );
            default:
                return cellValue;
        }
    }, []);

    return (
        <>
            <Table 
                aria-label="Trade history"
                classNames={{
                    wrapper: "!border-blue-100 border-[1px] shadow-none user-select-none overflow-x-auto",
                    tr: "border-b border-divider border-blue-100", 
                    th: "!bg-transparent border-b border-blue-100 text-[14px] text-black font-roboto font-[500] pb-4", 
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
                            <TableCell className="text-gray-800">
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