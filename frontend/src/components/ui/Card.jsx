import React from 'react';
import clsx from 'clsx';

export const Card = React.forwardRef(({
  children,
  className,
  hover = false,
  padding = 'md',
  ...props
}, ref) => {
  const paddingStyles = {
    none: '',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  };

  return (
    <div
      ref={ref}
      className={clsx(
        'bg-card-bg backdrop-blur-glass border border-glass-border rounded-2xl shadow-glass',
        hover && 'hover:border-primary-500 transition-all duration-200 hover:-translate-y-0.5',
        paddingStyles[padding],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
});

Card.displayName = 'Card';

export const CardHeader = ({ children, className }) => (
  <div className={`mb-4 ${className}`}>{children}</div>
);

export const CardTitle = ({ children, className }) => (
  <h3 className={`text-xl font-bold text-dark-100 ${className}`}>{children}</h3>
);

export const CardContent = ({ children, className }) => (
  <div className={className}>{children}</div>
);
