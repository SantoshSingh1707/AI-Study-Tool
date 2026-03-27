import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Badge } from '@/components/ui/Badge';

describe('Badge', () => {
  it('renders children', () => {
    render(<Badge>Status</Badge>);
    expect(screen.getByText('Status')).toBeInTheDocument();
  });

  it('applies default variant when not specified', () => {
    render(<Badge>Default</Badge>);
    expect(screen.getByText('Default')).toHaveClass('bg-dark-700');
  });

  it('applies easy variant correctly', () => {
    render(<Badge variant="easy">Easy</Badge>);
    expect(screen.getByText('Easy')).toHaveClass('bg-green-500/20', 'text-green-400');
  });

  it('applies medium variant correctly', () => {
    render(<Badge variant="medium">Medium</Badge>);
    expect(screen.getByText('Medium')).toHaveClass('bg-yellow-500/20', 'text-yellow-400');
  });

  it('applies hard variant correctly', () => {
    render(<Badge variant="hard">Hard</Badge>);
    expect(screen.getByText('Hard')).toHaveClass('bg-red-500/20', 'text-red-400');
  });

  it('applies mcq variant correctly', () => {
    render(<Badge variant="mcq">MCQ</Badge>);
    expect(screen.getByText('MCQ')).toHaveClass('bg-primary-500/20', 'text-primary-400');
  });

  it('applies truefalse variant correctly', () => {
    render(<Badge variant="truefalse">True/False</Badge>);
    expect(screen.getByText('True/False')).toHaveClass('bg-secondary-500/20', 'text-secondary-400');
  });

  it('applies custom className', () => {
    render(<Badge className="custom-badge">Test</Badge>);
    expect(screen.getByText('Test')).toHaveClass('custom-badge');
  });
});
