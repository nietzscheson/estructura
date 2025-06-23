import {
    Menu,
    useSidebarState,
    MenuItemLink,
  } from "react-admin";
  import SubscriptionsIcon from "@mui/icons-material/WorkspacePremium"; // o el ícono que prefieras
  import { useLocation } from "react-router-dom";
  
  export const CustomMenu = () => {
    const [open] = useSidebarState();
    const location = useLocation();
  
    return (
      <Menu>
        {/* Recursos normales */}
        <Menu.ResourceItem name="documents" />
        <Menu.ResourceItem name="workspaces" />
        <Menu.ResourceItem name="structures" />
        <Menu.ResourceItem name="keys" />
  
        {/* Enlace a la custom page */}
        <MenuItemLink
          to="/subscriptions"
          primaryText="Subscription"
          leftIcon={<SubscriptionsIcon />}
          sidebarIsOpen={open}
          selected={location.pathname === "/subscriptions"}
        />
      </Menu>
    );
  };
  