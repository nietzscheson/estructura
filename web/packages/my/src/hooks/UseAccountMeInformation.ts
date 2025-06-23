import { useEffect, useState } from 'react';
import { useDataProvider } from 'react-admin';
import { DataProvider } from 'react-admin';

export interface EstructuraDataProvider extends DataProvider {
  getAccountInfo: () => Promise<{
    plan: string;
    pages_limit: number;
    pages_used: number;
  }>;
}

export const useAccountInformation = () => {
  const [data, setData] = useState<null | {
    plan: string;
    pages_limit: number;
    pages_used: number;
  }>(null);

  const dataProvider = useDataProvider();

  useEffect(() => {
    const fetch = async () => {
      try {
        const result = await (dataProvider as EstructuraDataProvider).getAccountInfo();
        setData({
          plan: result.plan,
          pages_limit: result.pages_limit,
          pages_used: result.pages_used,
        });
      } catch (error) {
        console.error('Error fetching account info from dataProvider', error);
      }
    };

    fetch();
  }, [dataProvider]);

  return data;
};