import { Button } from "./ui/button"
import welcomepng from '@/assets/cinema-hero.jpg';
import { Combine } from "lucide-preact";

export default function Welcome() {
    return (
        <div class="relative min-h-screen overflow-hidden">
            {/* Background Image with Overlay */}
            <div className="absolute inset-0">
                <img
                    src={welcomepng}
                    alt="Cinema Background"
                    className="w-full h-full object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black via-black/70 to-black/30"></div>
                <div className="absolute inset-0 bg-gradient-to-r from-red-900/20 to-blue-900/20"></div>
            </div>

            {/* Content */}
            <div className="relative z-10 flex flex-col items-center justify-center min-h-screen p-8 text-center">
                {/* Logo/Brand */}
                <div className="mb-8">
                    <h1 className="text-6xl md:text-7xl font-bold bg-gradient-to-r from-red-500 via-yellow-500 to-red-600 bg-clip-text text-transparent mb-2">
                        CINEMA MAX
                    </h1>
                    <div className="w-32 h-1 bg-gradient-to-r from-red-500 to-yellow-500 mx-auto rounded-full"></div>
                </div>

                {/* Welcome Text */}
                <div className="max-w-4xl mb-12">
                    <h2 className="text-2xl md:text-3xl text-white font-semibold mb-4">
                        Welcome to the Ultimate Movie Experience
                        <span className="animate-caret-blink text-yellow-400 ml-2">|</span>
                    </h2>
                    <p className="text-lg md:text-xl text-gray-300 leading-relaxed max-w-2xl mx-auto">
                        Experience the magic of cinema like never before. Book your seats,
                        grab your popcorn, and dive into extraordinary stories that come alive on the big screen.
                    </p>
                </div>

                {/* Action Buttons */}
                <div className="flex flex-col sm:flex-row gap-4 mb-8">
                    <Button className="bg-red-600 hover:bg-red-700 text-white px-8 py-3 text-lg font-semibold rounded-full transition-all duration-300 transform hover:scale-105 shadow-lg">
                        Book Tickets Now
                    </Button>
                    <Button className="bg-transparent border-2 border-white text-white hover:bg-white hover:text-black px-8 py-3 text-lg font-semibold rounded-full transition-all duration-300">
                        Browse Movies
                    </Button>
                </div>

                {/* Features */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl w-full">
                    <div className="bg-black/40 backdrop-blur-sm p-6 rounded-lg border border-white/10">
                        <h3 className="text-xl font-semibold text-white mb-2">Premium Experience</h3>
                        <p className="text-gray-300">Luxury seating, crystal clear sound, and stunning visuals</p>
                    </div>
                    <div className="bg-black/40 backdrop-blur-sm p-6 rounded-lg border border-white/10">
                        <h3 className="text-xl font-semibold text-white mb-2">Easy Booking</h3>
                        <p className="text-gray-300">Book your tickets in seconds with our simple interface</p>
                    </div>
                    <div className="bg-black/40 backdrop-blur-sm p-6 rounded-lg border border-white/10">
                        <h3 className="text-xl font-semibold text-white mb-2">Complete Package</h3>
                        <p className="text-gray-300">Snacks, drinks, and entertainment all in one place</p>
                    </div>
                </div>

                {/* Scroll Indicator */}
                {/* <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2">
                    <div className="animate-bounce">
                        <div className="w-6 h-10 border-2 border-white/50 rounded-full flex justify-center">
                            <div className="w-1 h-3 bg-white/50 rounded-full mt-2 animate-pulse"></div>
                        </div>
                    </div>
                </div> */}
            </div>
        </div>
    )
}   
