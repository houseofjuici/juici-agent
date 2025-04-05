import React from 'react';
import Link from 'next/link';
import Head from 'next/head';

export default function Custom404() {
  return (
    <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
      <Head>
        <title>404 - Page Not Found | Juici Agents</title>
      </Head>
      <div className="text-center p-8">
        <h1 className="text-6xl font-bold mb-4">404</h1>
        <p className="text-xl mb-8">Oops! The page you're looking for cannot be found.</p>
        <Link href="/">
          <span className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg text-lg font-medium">
            Go back home
          </span>
        </Link>
      </div>
    </div>
  );
} 