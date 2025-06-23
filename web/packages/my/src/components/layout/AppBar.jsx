import {
  AppBar,
  UserMenu,
  useResourceDefinition,
  TitlePortal,
  useLogout,
  userLogout
} from 'react-admin';
import {
  MenuItem,
  Box,
  Typography,
  useMediaQuery,
} from '@mui/material';
import PowerSettingsNewIcon from '@mui/icons-material/PowerSettingsNew';
import { useTheme } from '@mui/material/styles';
import { FileJson2 } from 'lucide-react';

const CustomAppBar = (props) => {
  const theme = useTheme();
  const isSmall = useMediaQuery(theme.breakpoints.down('sm'));
  const resource = useResourceDefinition();

  return (
    <AppBar
      {...props}
      color="primary"
    >
      <Box display="flex" alignItems="center" width="100%">
        <Box display="flex" alignItems="center" gap={1}>
          <FileJson2 style={{ width: 28, height: 28, }} />
          <Typography variant="h6" fontWeight="bold">
            estructura
          </Typography>
          {!isSmall && (
            <Box
              sx={{
                height: 20,
                width: '1px',
                bgcolor: '#4B5563',
                mx: 2,
              }}
            />
          )}
          {!isSmall && (
            <Typography
              variant="subtitle1"
              fontWeight={400}
              sx={{ color: '#d1d5db' }}
            >
              {resource?.options?.label || resource?.name}
            </Typography>
          )}
        </Box>

        <TitlePortal />
      </Box>
    </AppBar>
  );
};

export default CustomAppBar;
