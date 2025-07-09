import { addToast, Button, Modal, ModalBody, ModalContent, Pagination, Table, TableBody, TableCell, TableColumn, TableHeader, TableRow, Tooltip, useDisclosure } from '@heroui/react';
import axios from 'axios';
import { useCallback, useMemo, useState, type ReactNode } from 'react';
import { FiArrowUpRight } from 'react-icons/fi';
import { MdDelete } from 'react-icons/md';
import type { ILocation } from '../../types';
import ItemsMap from '../common/ItemsMap';
import LocationsNewEdit from './LocationsNewEdit';

interface IProps {
    locations: ILocation[]
}

const LocationsTable = ({ locations }: IProps) => {
    const [locationToEdit, setLocationToEdit] = useState<ILocation | null>(null);
    const {isOpen, onOpen, onOpenChange} = useDisclosure();

    const openEditLocation = useCallback((locationEdit: ILocation) => {
        setLocationToEdit(locationEdit);
        onOpen();
    }, [onOpen]);

    const onDeleteLocation = useCallback(async (locationId: string) => {
        try {
            await axios.delete(`${import.meta.env.VITE_API_URL}/api/v1/locations/${locationId}`);
            addToast({ title: "Success!", description: "Location deleted successfully." });
            window.location.reload();
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        } catch (error: any) {
            if (error?.response?.status === 409) {
                addToast({ title: "Forbidden", description: "This location already has billboards assigned to it" });
            } else addToast({ title: "Error", description: "Oops, something went wrong" });
        }
    }, [])

    const columns = useMemo(() => ([
        {name: "Address", uid: "address"},
        {name: "City", uid: "city"},
        {name: "State", uid: "state"},
        {name: "Country", uid: "country_code"},
        {name: "", uid: "actions"},
    ]), []);

    const locationItems = useMemo(() => 
        !locations ? [] 
        : locations
    , [locations]);

    const [page, setPage] = useState(1);
    const rowsPerPage = 5;
    
    const pages = Math.ceil(locationItems.length / rowsPerPage);
    
    const items = useMemo(() => {
        const start = (page - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        return locationItems.slice(start, end);
    }, [page, locationItems]);

    const renderCell = useCallback((location: ILocation, columnKey: keyof Omit<ILocation, "links">) => {
        const cellValue = location[columnKey];
        switch (columnKey) {
            case "address":
                return (
                    <div className="flex">
                        <p className="text-bold text-sm mx-auto">
                            {cellValue} 
                        </p>
                    </div>
                );
            case "city":
                return (
                    <div className="flex">
                        <p className="text-bold text-sm mx-auto">
                            {cellValue} 
                        </p>
                    </div>
                );
            case "state":
                return (
                    <div className="flex">
                        <p className="text-bold text-sm mx-auto">
                            {cellValue} 
                        </p>
                    </div>
                );
            case "country_code":
                return (
                    <div className="flex">
                        <p className="text-bold text-sm mx-auto">
                            {cellValue} 
                        </p>
                    </div>
                );
            case "actions" as keyof ILocation:
                return (
                    <div className="flex items-center gap-2 justify-end">
                        <Tooltip content="Edit Location" showArrow={true}>
                            <Button isIconOnly variant="light" color="primary" 
                                onPress={() => openEditLocation(location)} 
                                className="rounded-[6px] !h-[32px] !max-w-[32px] !px-0 py-1"
                            >
                                <FiArrowUpRight size={18} color="#2F6BDC"/>
                            </Button>
                        </Tooltip>
                        <Tooltip content="Delete Location" showArrow={true}>
                            <Button isIconOnly variant="light" color="danger" 
                                onPress={() => onDeleteLocation(location?.id)} 
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
    }, [openEditLocation, onDeleteLocation]);

    return (
        <>
            <div className="w-full h-full flex flex-col gap-4">
                <Table 
                    aria-label="Locations table"
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
                                    {renderCell(item, columnKey as keyof Omit<ILocation, "links">) as ReactNode}
                                </TableCell>
                            )}
                        </TableRow>
                    )}
                    </TableBody>
                </Table>
                <ItemsMap items={items} />
            </div>
            <Modal className="bg-zinc-800 z-[1000]" isOpen={isOpen} onOpenChange={onOpenChange} size="5xl" scrollBehavior='outside'>
                <ModalContent className="p-2 sm:p-4">
                    <ModalBody>
                        <div className="h-full flex items-center gap-2">
                            <span className="text-[18px] sm:text-[24px] font-[500]">Edit Location</span>
                        </div>
                        <div className="w-full h-full flex grow justify-center items-center p-4 sm:p-[40px] border-[1px] border-blue-100 rounded-[9px] sm:rounded-[12px]">
                            <LocationsNewEdit onOpenChange={onOpenChange} location={locationToEdit} />
                        </div>
                    </ModalBody>
                </ModalContent>
            </Modal>
        </>
    )
}

export default LocationsTable