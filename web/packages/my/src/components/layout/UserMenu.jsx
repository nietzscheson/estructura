import { UserMenu, Logout } from 'react-admin';

import ProfileMenuItem from './ProfileMenuItem';

const CustomUserMenu = props => {
    <UserMenu {...props}>
        <ProfileMenuItem/>
        <Logout />
    </UserMenu>
}

export default CustomUserMenu;