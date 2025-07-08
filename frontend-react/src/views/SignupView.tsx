import { addToast, Button, Form, Input } from "@heroui/react";
import { zodResolver } from "@hookform/resolvers/zod";
import axios from "axios";
import { useState } from "react";
import { FormProvider, useForm } from "react-hook-form";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import { Link, useNavigate } from "react-router-dom";
import { z as zod } from "zod";
import type { ILoginForm } from "../types";

const SignupView = () => {
  const [showPass, setShowPass] = useState(false);  
  const navigate = useNavigate();  

  const LoginSchema = zod.object({
    email: zod.string().email({ message: "Not a valid email" }),
    password: zod
      .string()
      .min(1, { message: "Empty password not allowed" }),
  });

  const defaultValuesLogin: ILoginForm = {
    email: "",
    password: "",
  };

  const methods = useForm<ILoginForm>({
    resolver: zodResolver(LoginSchema),
    defaultValues: defaultValuesLogin,
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
        `${import.meta.env.VITE_API_URL}/api/v1/auth/sign-up`,
        data
        );
        if (response.status === 201) {
            addToast({
                title: "We sent you an email",
                description: "Please confirm your email",
            });
            navigate("/auth/signin");
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
    <div className="w-full h-full min-h-[100dvh] flex flex-col items-center justify-center gap-8">
        <h1 className="text-center text-[30px] font-[800] max-w-[340px]">Welcome to the Billboard Advertising App</h1>
        <div className="!w-[320px] p-y-4 rounded-lg p-4 border-[1px] border-gray-600 shadow-md">
            <FormProvider {...methods}>
              <Form onSubmit={onSubmit} className="flex flex-col gap-4">
                <Input
                  type="Email"
                  label="Email"
                  variant="bordered"
                  placeholder={"Insert your email"}
                  value={values.email}
                  onChange={(e) => setValue("email", e.target.value)}
                />
                <Input
                  type={showPass ? "text" : "password"}
                  variant="bordered"
                  label={"Password"}
                  placeholder={"Insert your password"}
                  endContent={
                    <button
                      aria-label="toggle password visibility"
                      className="focus:outline-none flex items-center justify-center my-auto !text-gray-100/50"
                      type="button"
                      onClick={() => setShowPass(!showPass)}
                    >
                      {showPass ? (
                        <FaEyeSlash size={24} />
                      ) : (
                        <FaEye size={24} />
                      )}
                    </button>
                  }
                  value={values.password}
                  onChange={(e) => setValue("password", e.target.value)}
                />
                {errors && (
                  <span className="w-full font-roboto text-sm text-red-600 align-center whitespace-pre-wrap">
                    {Object.values(errors).map(
                      (error) => `${error.message}\n`
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
                  Sign Up
                </Button>
                <div className="w-full flex justify-between items-end">
                  <div className="w-full flex flex-col gap-0">
                    <p>
                      {"Already have an account?"}{" "}
                    </p>
                    <Link className="text-blue-600" to="/auth/signin">{"Sign In"}</Link>
                  </div>
                </div>
              </Form>
            </FormProvider>
        </div>
    </div>
  )
}

export default SignupView