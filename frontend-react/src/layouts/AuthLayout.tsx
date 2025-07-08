
interface IProps {
    children: React.ReactNode
}

const AuthLayout = ({ children }: IProps) => {
  return (
    <div className="w-full h-full">
        {children}
    </div>
  )
}

export default AuthLayout