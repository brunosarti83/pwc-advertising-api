import { Button, Link, Navbar, NavbarBrand, NavbarContent, NavbarItem } from "@heroui/react";
import axios from "axios";
import { useCallback } from "react";
import { FaSign } from "react-icons/fa";
import { useLocation, useNavigate } from "react-router-dom";


const NavBar = () => {
    const navigate = useNavigate();
    const { pathname } = useLocation();

    const onSignOut = useCallback(async () => {
        await axios.post(`${import.meta.env.VITE_API_URL}/api/v1/auth/sign-out`);
        axios.defaults.headers.common["Authorization"] = "";
        navigate("/auth/signin");
    }, [navigate])

    return (
    <Navbar className="bg-zinc-900 z-[10000]">
      <NavbarBrand>
        <FaSign size={24} />
        <p className="font-bold font-roboto text-[24px]">PwC Advertising</p>
      </NavbarBrand>
      <NavbarContent className="hidden sm:flex gap-4" justify="center">
        <NavbarItem isActive={pathname.startsWith("/campaigns")}>
          <Link className="text-gray-50" color="foreground" href="/campaigns">
            Campaigns
          </Link>
        </NavbarItem>
        <NavbarItem isActive={pathname.startsWith("/billboards")}>
          <Link className="text-gray-50" href="/billboards">
            Billboards
          </Link>
        </NavbarItem>
        <NavbarItem isActive={pathname.startsWith("/locations")}>
          <Link className="text-gray-50" color="foreground" href="/locations">
            Locations
          </Link>
        </NavbarItem>
      </NavbarContent>
      <NavbarContent justify="end">
        <NavbarItem>
          <Button onPress={onSignOut} color="primary" href="#" variant="flat">
            Sign Out
          </Button>
        </NavbarItem>
      </NavbarContent>
    </Navbar>
  );
}

export default NavBar