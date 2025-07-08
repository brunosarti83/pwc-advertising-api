import { addToast, Button, Form, Input, Select, SelectItem } from "@heroui/react";
import { zodResolver } from "@hookform/resolvers/zod";
import axios from "axios";
import { useEffect, useState } from "react";
import { FormProvider, useForm } from "react-hook-form";
import { z as zod } from "zod";
import type { ILocation, INewBillboard } from "../../types";

interface IProps {
  onOpenChange: () => void;
}
const BillboardsNew = ({ onOpenChange }: IProps) => {  
  const [locations, setLocations] = useState<ILocation[]>([]);
  const [selected, setSelected] = useState<string>("");
  
  useEffect(() => {
    const fetchLocations = async () => {
      try {
        const response = await axios.get(
          `${import.meta.env.VITE_API_URL}/api/v1/locations`
        );
        if (response.status === 200) {
          setLocations(response.data.data);
        }
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      } catch (error) {
        addToast({ title: "Error", description: "Failed to load locations" });
      }
    };

    fetchLocations();
  }, []); 

  const NewBillboardSchema = zod.object({
    location_id: zod.string(),
    width_mt: zod
      .number()
      .min(1, { message: "Min Width 1 mt" }),
    height_mt: zod
      .number()
      .min(1, { message: "Min Height 1 mt" }),
    dollars_per_day: zod
      .number()
      .min(1, { message: "Min 1.00 dollar per day" }),
  });

  const defaultValuesNewBillboard: INewBillboard = {
    location_id: "",
    width_mt: 0,
    height_mt: 0,
    dollars_per_day: 0
  };

  const methods = useForm<INewBillboard>({
    resolver: zodResolver(NewBillboardSchema),
    defaultValues: defaultValuesNewBillboard,
  });

  const {
    watch,
    setValue,
    handleSubmit,
    formState: { isSubmitting, errors },
  } = methods;

  const values = watch();

  useEffect(() => setValue("location_id", selected), [selected, setValue]);

  const onSubmit = handleSubmit(
    async (data) => {
      try {
        const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/api/v1/billboards`,
        data
        );
        if (response.status === 201) {
            addToast({
                title: "Billboard created!"
            });
            onOpenChange();
            // Reload the page to see the new billboard
            window.location.reload();
        }
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      } catch (error) {
        addToast({ title: "Error", description: "Oops, something went wrong" });
      }
    },
    () => {
      addToast({ title: "Error", description: "Oops, something went wrong" });
    }
  );
  return (
    <div className="w-full h-full flex flex-col items-center justify-center gap-8 !text-gray-50">
        <div className="w-full p-y-4 rounded-lg p-4">
            <FormProvider {...methods}>
              <Form onSubmit={onSubmit} className="flex flex-col gap-4">
                <Select
                  label="Location"
                  placeholder={locations.length ? "Select a location" : "Loading locations..."}
                  variant="bordered"
                  selectedKeys={[selected]}
                  onChange={(e) => { console.log(e.target.value); setSelected(e.target.value)}}
                >
                    { locations?.map((loc) => (
                        <SelectItem key={loc?.id} textValue={`${loc?.address}, ${loc?.city}, ${loc?.state} (${loc?.country_code})`}>
                            {`${loc?.address}, ${loc?.city}, ${loc?.state} (${loc?.country_code})`}
                        </SelectItem>
                    ))}
                </Select>        
                <Input
                  label="Width (mt)"
                  variant="bordered"
                  type="number"
                  placeholder={"Enter width in meters"}
                  value={values.width_mt.toString()}
                  onChange={(e) => setValue("width_mt", Number(e.target.value))}
                />
                <Input
                  label="Height (mt)"
                  variant="bordered"
                  placeholder={"Enter height in meters"}
                  type="number"
                  value={values.height_mt.toString()}
                  onChange={(e) => setValue("height_mt", Number(e.target.value))}
                />
                <Input
                  label="Dollars per day"
                  variant="bordered"
                  type="number"
                  startContent={
                        <div className="pointer-events-none flex items-center">
                        <span className="text-default-400 text-small">$</span>
                        </div>
                    }
                  placeholder={"Enter price per day"}
                  value={values.dollars_per_day.toString()}
                  onChange={(e) => setValue("dollars_per_day", Number(e.target.value))}
                />
                {errors && (
                  <span className="w-full font-roboto text-sm text-red-600 align-center whitespace-pre-wrap">
                    {Object.values(errors).map(
                      (error) => `${error?.message}\n`
                    )}
                  </span>
                )}
                <Button
                  id="btn-login"
                  isLoading={isSubmitting}
                  type="submit"
                  color="primary"
                  radius="sm"
                  className="w-full"
                >
                  Create
                </Button>
              </Form>
            </FormProvider>
        </div>
    </div>
  )
}

export default BillboardsNew