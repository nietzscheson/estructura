"use client";
import { NextPage } from 'next';
import dynamic from 'next/dynamic';

const AdminPage = dynamic(() => import('@/components/AdminApp'), {ssr: false,});

const Home: NextPage = () => <AdminPage />;

export default Home;