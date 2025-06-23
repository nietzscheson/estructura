import { defaultDarkTheme } from 'react-admin';
import { createTheme, ThemeOptions } from '@mui/material/styles';

export const DarkTheme = createTheme({
  ...defaultDarkTheme,
  palette: {
    ...defaultDarkTheme.palette,
    primary: {
      main: '#10b981', // Emerald green (Tailwind emerald-500)
    },
    background: {
      default: '#0b0b0b', // Tailwind gray-900
      paper: '#0b0b0b',    // Tailwind gray-800
    },
    text: {
      primary: '#ffffff',
      secondary: '#d1d5db', // Tailwind gray-300
    },
  },
  components: {
    ...defaultDarkTheme.components,
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#0b0b0b',
        },
      },
    },
  },
} as ThemeOptions);
