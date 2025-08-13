import "./App.css";
import Welcome from "./components/Welcome";
import { Button } from "./components/Button";

export const App = () => {
    return (
        <div>
            <Welcome />
            <div class="bg-gradient-to-br from-slate-900 to-stone-500 p-8 space-x-4 text-white text-2xl font-bold min-h-screen flex items-center justify-center">
                <Button variant="primary" onClick={() => alert('Primary clicked!')}>
                    Primary Button
                </Button>
                <Button variant="secondary" onClick={() => alert('Secondary clicked!')}>
                    Secondary Button
                </Button>
                <Button variant="tertiary" onClick={() => alert('Tertiary clicked!')}>
                    Tertiary Button
                </Button>
                <Button disabled>
                    Disabled Button
                </Button>
            </div>
        </div>
    );
}