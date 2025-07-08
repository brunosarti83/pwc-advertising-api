import { addToast, Button, Form, Input } from "@heroui/react";
import { zodResolver } from "@hookform/resolvers/zod";
import axios from "axios";
import { FormProvider, useForm } from "react-hook-form";
import { z as zod } from "zod";
import type { INewLocation } from "../../types";

interface IProps {
  onOpenChange: () => void;
}
const LocationsNew = ({ onOpenChange }: IProps) => {  
  
  const NewLocationSchema = zod.object({
    address: zod.string(),
    city: zod.string(),
    state: zod.string(),
    country_code: zod.string(),
    lat: zod.number().min(-90).max(90, { message: "Latitude must be between -90 and 90" }),
    lng: zod.number().min(-180).max(180, { message: "Longitude must be between -180 and 180" }),
  });

  const defaultValuesNewLocation: INewLocation = {
    address: "",
    city: "",
    state: "",
    country_code: "",
    lat: 0,
    lng: 0
  };

  const methods = useForm<INewLocation>({
    resolver: zodResolver(NewLocationSchema),
    defaultValues: defaultValuesNewLocation,
  });

  const {
    watch,
    setValue,
    handleSubmit,
    formState: { isSubmitting, errors },
  } = methods;

  const values = watch();

  const onSubmit = handleSubmit(
    async (data) => {
      try {
        const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/api/v1/locations`,
        data
        );
        if (response.status === 201) {
            addToast({
                title: "Location created!"
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
                <Input
                  label="Address"
                  variant="bordered"
                  placeholder={"Enter address"}
                  value={values.address}
                  onChange={(e) => setValue("address", e.target.value)}
                />       
                <Input
                  label="City"
                  variant="bordered"
                  placeholder={"Enter city"}
                  value={values.city}
                  onChange={(e) => setValue("city", e.target.value)}
                />
                <Input
                  label="State"
                  variant="bordered"
                  placeholder={"Enter state"}
                  value={values.state}
                  onChange={(e) => setValue("state", e.target.value)}
                />
                <Input
                  label="Country Code"
                  variant="bordered"
                  placeholder={"Enter country code"}
                  value={values.country_code}
                  onChange={(e) => setValue("country_code", e.target.value)}
                />
                <Input
                  label="Latitude"
                  variant="bordered"
                  type="number"
                  placeholder={"Enter latitude"}
                  value={values.lat.toString()}
                  onChange={(e) => setValue("lat", Number(e.target.value))}
                />
                <Input
                  label="Longitude"
                  variant="bordered"
                  type="number"
                  placeholder={"Enter longitude"}
                  value={values.lng.toString()}
                  onChange={(e) => setValue("lng", Number(e.target.value))}
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

export default LocationsNew