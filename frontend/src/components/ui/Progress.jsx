import React from 'react';
import clsx from 'clsx';

export const Progress = ({
  value,
  max = 100,
  showLabel = false,
  variant = 'default',
  size = 'md',
  className,
}) => {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);

  const heights = {
    sm: 'h-1',
    md: 'h-2',
    lg: 'h-3',
  };

  const gradients = {
    default: 'from-primary-500 to-secondary-500',
    success: 'from-green-500 to-green-400',
    warning: 'from-yellow-500 to-yellow-400',
    danger: 'from-red-500 to-red-400',
  };

  return (
    <div className={clsx('w-full', className)}>
      <div
        className={clsx(
          'bg-dark-700 rounded-full overflow-hidden',
          heights[size]
        )}
      >
        <div
          className={clsx(
            'h-full bg-gradient-to-r transition-all duration-500',
            gradients[variant]
          )}
          style={{ width: `${percentage}%` }}
        />
      </div>
      {showLabel && (
        <p className="mt-1 text-sm text-dark-400 text-right">
          {Math.round(percentage)}%
        </p>
      )}
    </div>
  );
};
