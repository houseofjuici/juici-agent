import React from 'react';
import Link from 'next/link';

function Error({ statusCode }) {
  return (
    <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
      <div className="text-center p-8">
        <h1 className="text-6xl font-bold mb-4">
          {statusCode ? `${statusCode} Error` : 'An Error Occurred'}
        </h1>
        <p className="text-xl mb-8">
          {statusCode === 404 
            ? "Sorry, we couldn't find the page you're looking for." 
            : "Sorry, something went wrong on our server."}
        </p>
        <Link href="/">
          <span className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg text-lg font-medium">
            Return to Home
          </span>
        </Link>
      </div>
    </div>
  );
}

Error.getInitialProps = ({ res, err }) => {
  const statusCode = res ? res.statusCode : err ? err.statusCode : 404;
  return { statusCode };
};

export default Error; 