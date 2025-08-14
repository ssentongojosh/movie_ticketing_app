import type { ComponentChildren } from 'preact';

type ButtonProps = {
    children: ComponentChildren;
    variant?: 'primary' | 'secondary' | 'tertiary';
    onClick?: () => void;
    disabled?: boolean;
    className?: string;
};

const variantStyles: Record<string, string> = {
    primary: 'bg-purple-500 text-white hover:bg-purple-600 focus:ring-purple-500',
    secondary: 'bg-gray-500 text-white hover:bg-gray-600 focus:ring-gray-500',
    tertiary: 'bg-transparent text-purple-500 hover:bg-purple-100 focus:ring-purple-500',
};

export function Button({
    children,
    variant = 'primary',
    onClick,
    disabled = false,
    className = '',
}: ButtonProps) {
    const baseStyles = 'px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors';
    const disabledStyles = disabled ? 'opacity-50 cursor-not-allowed' : '';
    const styles = `${baseStyles} ${variantStyles[variant]} ${disabledStyles} ${className}`;
    
    return (
        <button
            class={styles}
            onClick={onClick}
            disabled={disabled}
            type="button"
        >
            {children}
        </button>
    );
}
