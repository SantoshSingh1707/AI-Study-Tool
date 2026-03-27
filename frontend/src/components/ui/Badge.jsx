import React from 'react';
import clsx from 'clsx';

export const Badge = ({
  children,
  variant = 'default',
  className,
}) => {
  const variants = {
    easy: 'bg-green-500/20 text-green-400 border border-green-500/30',
    medium: 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30',
    hard: 'bg-red-500/20 text-red-400 border border-red-500/30',
    mcq: 'bg-primary-500/20 text-primary-400 border border-primary-500/30',
    truefalse: 'bg-secondary-500/20 text-secondary-400 border border-secondary-500/30',
    default: 'bg-dark-700 text-dark-300 border border-dark-600',
  };

  return (
    <span
      className={clsx(
        'inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold',
        variants[variant],
        className
      )}
    >
      {children}
    </span>
  );
};
