// src/components/AccountSummary.tsx
import { Typography, Paper, Box, LinearProgress } from '@mui/material';
import { useAccountInformation } from '@/hooks/UseAccountMeInformation';

export const AccountSummary = () => {
  const account = useAccountInformation();

  if (!account) return null;

  const percentage = Math.min(
    (account.pages_used / account.pages_limit) * 100,
    100
  );

  return (
    <Paper
      elevation={1}
      sx={{
        width: '100%',
        boxSizing: 'border-box',
        backgroundColor: '#1f2937',
        color: '#fff',
      }}
    >
      <Box p={2} pr={4} display="flex" flexDirection="column" gap={1}>
        {/* Plan */}
        <Typography variant="body2">
          <strong>Plan:</strong> {account.plan}
        </Typography>

        {/* Progress bar */}
        <LinearProgress
          variant="determinate"
          value={percentage}
          sx={{
            height: 4,
            borderRadius: 2,
            backgroundColor: '#374151',
            '& .MuiLinearProgress-bar': {
              backgroundColor: '#22c55e',
            },
          }}
        />

        {/* Usage */}
        <Typography variant="body2">
          Usage: {account.pages_used} / {account.pages_limit} pages
        </Typography>
      </Box>
    </Paper>
  );
};
