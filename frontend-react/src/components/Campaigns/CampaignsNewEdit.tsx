import { addToast, Button, DatePicker, Form, Input } from "@heroui/react";
import { zodResolver } from "@hookform/resolvers/zod";
import { parseDate } from "@internationalized/date";
import axios from "axios";
import { FormProvider, useForm } from "react-hook-form";
import { z as zod } from "zod";
import type { ICampaign, INewCampaign } from "../../types";

interface IProps {
  onOpenChange: () => void;
  campaign?: ICampaign | null;
}
const CampaignsNewEdit = ({ onOpenChange, campaign }: IProps) => {  

  const NewCampaignSchema = zod.object({
    name: zod.string().min(1, { message: "Name is required" }),
    start_date: zod.string().min(1, { message: "Start date is required" }),
    end_date: zod.string().min(1, { message: "End date is required" }),
  });

  const defaultValuesNewCampaign: INewCampaign = {
    name: campaign?.name || "",
    start_date: campaign?.start_date || new Date().toISOString().split("T")[0],
    end_date: campaign?.end_date || new Date(new Date().setDate(new Date().getDate() + 30)).toISOString().split("T")[0],
  };

  const methods = useForm<INewCampaign>({
    resolver: zodResolver(NewCampaignSchema),
    defaultValues: defaultValuesNewCampaign,
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
        if (!campaign) await axios.post(`${import.meta.env.VITE_API_URL}/api/v1/campaigns`, data);
        else await axios.patch(`${import.meta.env.VITE_API_URL}/api/v1/campaigns/${campaign?.id}`, data);
        addToast({ title: "Success!" });
        onOpenChange();
        window.location.reload();
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
                  label="Name"
                  variant="bordered"
                  placeholder={"Enter campaign name"}
                  value={values.name}
                  onChange={(e) => setValue("name", e.target.value)}
                />
                <DatePicker
                    className="max-w-[284px]"
                    label="Date (controlled)"
                    variant="bordered"
                    value={parseDate(values.start_date)}
                    onChange={(val) => val ? setValue("start_date", val.toString()) : null}
                />
                <DatePicker
                    className="max-w-[284px]"
                    label="Date (controlled)"
                    variant="bordered"
                    value={parseDate(values.end_date)}
                    onChange={(val) => val ? setValue("end_date", val.toString()) : null}
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

export default CampaignsNewEdit