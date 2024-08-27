import React from "react";

const Logo = ({ width = 100, height = 100 }) => {
  return (
    <svg
      width={width}
      height={height}
      viewBox="0 0 200 200"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <circle cx="100" cy="100" r="100" fill="#007BFF" />
      <path
        d="M150 60C150 60 130 40 100 60C70 80 50 100 50 100C50 100 70 120 100 140C130 160 150 140 150 140"
        stroke="white"
        strokeWidth="10"
        strokeLinecap="round"
      />
      <circle cx="75" cy="80" r="10" fill="white" />
      <circle cx="125" cy="80" r="10" fill="white" />
    </svg>
  );
};

export default Logo;
