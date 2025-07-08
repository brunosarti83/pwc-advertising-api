import NavBar from "../components/NavBar/NavBar"

interface IProps {
    children: React.ReactNode
}

const MainLayout = ({ children }: IProps) => {
  return (
    <div className="w-full h-full flex flex-col gap-8">
        <NavBar />
        {children}
    </div>
  )
}

export default MainLayout