import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Progress } from '@/components/ui/Progress';

describe('Progress', () => {
  it('renders with default value 0', () => {
    render(<Progress value={0} />);
    const bar = document.querySelector('.bg-gradient-to-r');
    expect(bar).toHaveStyle({ width: '0%' });
  });

  it('renders at 50%', () => {
    render(<Progress value={50} max={100} />);
    const bar = document.querySelector('.bg-gradient-to-r');
    expect(bar).toHaveStyle({ width: '50%' });
  });

  it('clamps value above 100%', () => {
    render(<Progress value={150} max={100} />);
    const bar = document.querySelector('.bg-gradient-to-r');
    expect(bar).toHaveStyle({ width: '100%' });
  });

  it('clamps negative value', () => {
    render(<Progress value={-10} max={100} />);
    const bar = document.querySelector('.bg-gradient-to-r');
    expect(bar).toHaveStyle({ width: '0%' });
  });

  it('shows label when showLabel is true', () => {
    render(<Progress value={75} showLabel />);
    expect(screen.getByText('75%')).toBeInTheDocument();
  });

  it('hides label by default', () => {
    render(<Progress value={75} />);
    expect(screen.queryByText('75%')).not.toBeInTheDocument();
  });

  it('applies correct size class', () => {
    const { rerender } = render(<Progress value={50} size="sm" />);
    expect(screen.getByRole('progressbar')).toHaveClass('h-1');

    rerender(<Progress value={50} size="lg" />);
    expect(screen.getByRole('progressbar')).toHaveClass('h-3');
  });

  it('applies variant classes correctly', () => {
    const { rerender } = render(<Progress value={50} variant="success" />);
    expect(screen.getByRole('progressbar')).toHaveClass('from-green-500');

    rerender(<Progress value={50} variant="warning" />);
    expect(screen.getByRole('progressbar')).toHaveClass('from-yellow-500');

    rerender(<Progress value={50} variant="danger" />);
    expect(screen.getByRole('progressbar')).toHaveClass('from-red-500');
  });
});
