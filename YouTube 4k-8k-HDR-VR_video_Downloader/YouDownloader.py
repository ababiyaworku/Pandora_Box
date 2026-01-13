#!/usr/bin/env python3
"""
YouDownloader: Interactive YouTube/Video Downloader Tool
Enhanced user-friendly version with VR/3D/HDR format support
"""

import sys
import os
import re
from pathlib import Path
import json

try:
    import yt_dlp
except ImportError:
    print("❌ Error: yt-dlp is not installed.")
    print("📦 Install it with: pip install yt-dlp")
    input("Press Enter to exit...")
    sys.exit(1)

class YouDownloader:
    def __init__(self):
        self.download_dir = "downloads"
        self.url = None
        self.formats = []
        
    def print_banner(self):
        """Display welcome banner"""
        print("=" * 60)
        print("🎥 YOUDOWNLOADER - Interactive Video Downloader 🎵")
        print("=" * 60)
        print("📱 Supports YouTube, TikTok, Instagram, Twitter & 1000+ sites")
        print("🎯 Easy format selection with VR/3D/HDR support")
        print("-" * 60)
    
    def validate_url(self, url):
        """Enhanced URL validation"""
        if not url or not url.strip():
            return False
            
        url = url.strip()
        
        # Basic URL pattern
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return url_pattern.match(url) is not None
    
    def detect_video_type(self, fmt, info):
        """Detect special video types like VR, 360°, 3D, HDR with enhanced 3D 180° detection"""
        format_note = fmt.get('format_note', '').lower()
        format_id = fmt.get('format_id', '').lower()
        title = info.get('title', '').lower() if info else ''
        description = info.get('description', '').lower() if info else ''
        
        video_type = []
        
        # Enhanced 3D detection with specific formats
        stereo_keywords = {
            '3d': '3D',
            'stereoscopic': '3D',
            'stereo': '3D', 
            'sbs': 'SBS-3D',
            'side by side': 'SBS-3D',
            'side-by-side': 'SBS-3D',
            'top bottom': 'TB-3D',
            'top-bottom': 'TB-3D',
            'anaglyph': 'Anaglyph-3D',
            'dual fisheye': 'DualFisheye-3D'
        }
        
        for keyword, format_type in stereo_keywords.items():
            if keyword in format_note or keyword in title or keyword in description:
                video_type.append(format_type)
                break  # Only add one 3D type
        
        # Enhanced VR detection with specific types
        vr_keywords = {
            '360': '360°',
            'vr': 'VR',
            'virtual reality': 'VR',
            'spherical': '360°',
            'equirectangular': '360°-EQR'
        }
        
        for keyword, format_type in vr_keywords.items():
            if keyword in format_note or keyword in title or keyword in description:
                if format_type not in video_type:
                    video_type.append(format_type)
        
        # Enhanced 180° VR detection
        vr180_keywords = ['180', 'vr180', 'half sphere', 'hemispherical']
        for keyword in vr180_keywords:
            if keyword in format_note or keyword in title or keyword in description:
                if '180°' not in video_type:
                    video_type.append('180°')
        
        # Check for HDR content
        hdr_keywords = ['hdr', 'hdr10', 'hdr10+', 'dolby vision', 'high dynamic range', 'rec2020', 'bt2020']
        for keyword in hdr_keywords:
            if keyword in format_note or keyword in format_id:
                if 'HDR' not in video_type:
                    video_type.append('HDR')
        
        # Special combination detection for 3D 180° VR
        if any('3D' in vtype for vtype in video_type) and '180°' in video_type:
            # This is 3D 180° content - prioritize this combination
            video_type = ['3D-180°-VR'] + [vtype for vtype in video_type if '3D' not in vtype and vtype != '180°']
        
        return video_type
    
    def get_enhanced_resolution_info(self, fmt):
        """Get enhanced resolution information with special format detection"""
        height = fmt.get('height')
        width = fmt.get('width')
        
        if height and width:
            # Standard resolution categories
            if height >= 4320:
                base_res = "8K"
            elif height >= 2160:
                base_res = "4K"
            elif height >= 1440:
                base_res = "2K"
            elif height >= 1080:
                base_res = "1080p"
            elif height >= 720:
                base_res = "720p"
            else:
                base_res = f"{height}p"
            
            return f"{base_res} ({width}x{height})"
        else:
            return fmt.get('resolution', 'Unknown resolution')
    
    def get_video_info(self, url):
        """Fetch video information and available formats"""
        print("\n🔍 Fetching video information...")
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extractflat': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if not info:
                    return None, [], []
                
                # Get available formats
                formats = info.get('formats', [])
                
                # Filter and organize formats
                video_formats = []
                audio_formats = []
                
                for fmt in formats:
                    # Detect special video types for all formats
                    video_types = self.detect_video_type(fmt, info)
                    
                    if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none':
                        # Video + Audio format
                        video_formats.append({
                            'format_id': fmt['format_id'],
                            'ext': fmt['ext'],
                            'resolution': fmt.get('resolution', 'unknown'),
                            'height': fmt.get('height'),
                            'width': fmt.get('width'),
                            'filesize': fmt.get('filesize'),
                            'vcodec': fmt.get('vcodec', 'unknown'),
                            'acodec': fmt.get('acodec', 'unknown'),
                            'fps': fmt.get('fps'),
                            'vbr': fmt.get('vbr'),
                            'abr': fmt.get('abr'),
                            'type': 'video+audio',
                            'video_types': video_types,
                            'format_note': fmt.get('format_note', '')
                        })
                    elif fmt.get('vcodec') != 'none' and fmt.get('acodec') == 'none':
                        # Video only format
                        video_formats.append({
                            'format_id': fmt['format_id'],
                            'ext': fmt['ext'],
                            'resolution': fmt.get('resolution', 'unknown'),
                            'height': fmt.get('height'),
                            'width': fmt.get('width'),
                            'filesize': fmt.get('filesize'),
                            'vcodec': fmt.get('vcodec', 'unknown'),
                            'fps': fmt.get('fps'),
                            'vbr': fmt.get('vbr'),
                            'type': 'video_only',
                            'video_types': video_types,
                            'format_note': fmt.get('format_note', '')
                        })
                    elif fmt.get('acodec') != 'none' and fmt.get('vcodec') == 'none':
                        # Audio only format
                        audio_formats.append({
                            'format_id': fmt['format_id'],
                            'ext': fmt['ext'],
                            'abr': fmt.get('abr'),
                            'filesize': fmt.get('filesize'),
                            'acodec': fmt.get('acodec', 'unknown'),
                            'type': 'audio'
                        })
                
                return info, video_formats, audio_formats
                
        except yt_dlp.DownloadError as e:
            print(f"❌ Error fetching video info: {e}")
            return None, [], []
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None, [], []
    
    def format_filesize(self, size):
        """Convert bytes to human readable format"""
        if not size:
            return "Unknown size"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def display_video_info(self, info):
        """Display video information"""
        print("\n" + "=" * 50)
        print("📹 VIDEO INFORMATION")
        print("=" * 50)
        print(f"📺 Title: {info.get('title', 'Unknown')}")
        print(f"👤 Uploader: {info.get('uploader', 'Unknown')}")
        print(f"⏱️  Duration: {self.format_duration(info.get('duration', 0))}")
        print(f"👀 Views: {info.get('view_count', 'Unknown'):,}" if info.get('view_count') else "👀 Views: Unknown")
        print(f"📅 Upload Date: {info.get('upload_date', 'Unknown')}")
        if info.get('description'):
            desc = info['description'][:200] + "..." if len(info['description']) > 200 else info['description']
            print(f"📝 Description: {desc}")
    
    def format_duration(self, seconds):
        """Format duration in seconds to HH:MM:SS"""
        if not seconds:
            return "Unknown"
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    def display_format_options(self, video_formats, audio_formats, info):
        """Display all available download options"""
        print("\n" + "=" * 70)
        print("📋 AVAILABLE DOWNLOAD OPTIONS")
        print("=" * 70)
        
        options = []
        option_num = 1
        
        # Check if this is VR/360 content
        is_vr_content = False
        if info:
            title = info.get('title', '').lower()
            description = info.get('description', '').lower()
            vr_indicators = ['360', 'vr', '180', '3d', 'stereoscopic', 'virtual reality']
            is_vr_content = any(indicator in title or indicator in description for indicator in vr_indicators)
        
        # Special format options for VR content
        if is_vr_content:
            print("🌟 SPECIAL VR/3D FORMAT OPTIONS:")
            print("-" * 30)
            
            # Check specifically for 3D 180° content
            has_3d_180 = any('3d' in title and '180' in title for title in [title, description])
            has_sbs = any('sbs' in text or 'side by side' in text or 'side-by-side' in text 
                         for text in [title, description, str(video_formats)])
            
            if has_3d_180 or has_sbs:
                options.append({
                    'num': option_num,
                    'description': '🥽 Best 3D 180° VR (Side-by-Side MKV)',
                    'format': 'bestvideo+bestaudio/best',
                    'ext': 'mkv',
                    'type': '3d_180_sbs_video'
                })
                print(f"{option_num}. 🥽 Best 3D 180° VR (Side-by-Side MKV)")
                option_num += 1
            
            options.append({
                'num': option_num,
                'description': '🌐 Best 360° VR Video (MKV)',
                'format': 'bestvideo+bestaudio/best',
                'ext': 'mkv',
                'type': 'vr_360_video'
            })
            print(f"{option_num}. 🌐 Best 360° VR Video (MKV)")
            option_num += 1
            
            options.append({
                'num': option_num,
                'description': '📹 Best 180° VR Video (MKV)',
                'format': 'bestvideo+bestaudio/best',
                'ext': 'mkv',
                'type': 'vr_180_video'
            })
            print(f"{option_num}. 📹 Best 180° VR Video (MKV)")
            option_num += 1
            
            options.append({
                'num': option_num,
                'description': '🥽 Best 3D Stereoscopic Video (MKV)',
                'format': 'bestvideo+bestaudio/best',
                'ext': 'mkv',
                'type': '3d_video'
            })
            print(f"{option_num}. 🥽 Best 3D Stereoscopic Video (MKV)")
            option_num += 1
        
        # Standard quality options
        print(f"\n🚀 STANDARD OPTIONS:")
        print("-" * 30)
        
        # Best video + audio (MKV for highest quality)
        options.append({
            'num': option_num,
            'description': '🎬 Best Quality Video (MKV - Supports 4K/8K/HDR)',
            'format': 'bestvideo+bestaudio/best',
            'ext': 'mkv',
            'type': 'quick_video_mkv'
        })
        print(f"{option_num}. 🎬 Best Quality Video (MKV - Supports 4K/8K/HDR)")
        option_num += 1
        
        # Best video MP4 (more compatible but lower quality)
        options.append({
            'num': option_num,
            'description': '🎬 Best Quality Video (MP4 - More Compatible)',
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'ext': 'mp4',
            'type': 'quick_video_mp4'
        })
        print(f"{option_num}. 🎬 Best Quality Video (MP4 - More Compatible)")
        option_num += 1
        
        # Best audio
        options.append({
            'num': option_num,
            'description': '🎵 Best Quality Audio (MP3 320kbps)',
            'format': 'bestaudio/best',
            'ext': 'mp3',
            'type': 'quick_audio'
        })
        print(f"{option_num}. 🎵 Best Quality Audio (MP3 320kbps)")
        option_num += 1
        
        # Audio formats
        if audio_formats:
            print(f"\n🎵 AUDIO FORMATS:")
            print("-" * 30)
            
            # Sort by bitrate (descending), handle None values
            audio_formats.sort(key=lambda x: x.get('abr') or 0, reverse=True)
            
            displayed_audio = set()
            for fmt in audio_formats:
                key = f"{fmt['ext']}_{fmt.get('abr', 0)}"
                if key not in displayed_audio:
                    displayed_audio.add(key)
                    
                    options.append({
                        'num': option_num,
                        'format': fmt['format_id'],
                        'ext': fmt['ext'],
                        'type': 'audio',
                        'info': fmt
                    })
                    
                    bitrate = f"{fmt.get('abr')}kbps" if fmt.get('abr') else "Unknown bitrate"
                    size = self.format_filesize(fmt.get('filesize'))
                    codec = fmt.get('acodec', 'unknown')
                    
                    print(f"{option_num}. 🎵 {fmt['ext'].upper()} - {bitrate} ({codec}) [{size}]")
                    option_num += 1
        
        # Video formats with enhanced VR/3D/HDR detection
        if video_formats:
            print(f"\n🎬 VIDEO FORMATS:")
            print("-" * 30)
            
            # Sort by special types first, then resolution and fps
            def sort_key(fmt):
                special_priority = 0
                if fmt.get('video_types'):
                    # Higher priority for 3D 180° combinations
                    if 'SBS-3D' in fmt['video_types'] and '180°' in fmt['video_types']:
                        special_priority += 2000
                    elif '3D-180°-VR' in fmt['video_types']:
                        special_priority += 1800
                    elif 'SBS-3D' in fmt['video_types']:
                        special_priority += 1500
                    elif 'HDR' in fmt['video_types']:
                        special_priority += 1000
                    elif '360°' in fmt['video_types'] or 'VR' in fmt['video_types']:
                        special_priority += 500
                    elif any('3D' in vtype for vtype in fmt['video_types']):
                        special_priority += 300
                    elif '180°' in fmt['video_types']:
                        special_priority += 200
                
                return (
                    special_priority,
                    fmt.get('height') or 0,
                    fmt.get('fps') or 0,
                    fmt.get('vbr') or 0
                )
            
            video_formats.sort(key=sort_key, reverse=True)
            
            displayed_video = set()
            for fmt in video_formats:
                special_types_str = '+'.join(fmt.get('video_types', []))
                key = f"{fmt['ext']}_{fmt.get('height', 0)}_{fmt.get('fps', 0)}_{fmt.get('vcodec', 'unknown')[:10]}_{special_types_str}"
                
                if key not in displayed_video and len(displayed_video) < 20:
                    displayed_video.add(key)
                    
                    options.append({
                        'num': option_num,
                        'format': fmt['format_id'],
                        'ext': fmt['ext'],
                        'type': 'video',
                        'info': fmt
                    })
                    
                    # Enhanced resolution display with special format detection
                    res_display = self.get_enhanced_resolution_info(fmt)
                    
                    # Add special format tags with enhanced 3D 180° detection
                    special_tags = []
                    if fmt.get('video_types'):
                        for vtype in fmt['video_types']:
                            if vtype == '3D-180°-VR':
                                special_tags.append('🥽3D-180°-VR')
                            elif vtype == 'SBS-3D':
                                special_tags.append('🥽SBS-3D')
                            elif vtype == 'TB-3D':
                                special_tags.append('🥽TB-3D')
                            elif vtype == 'DualFisheye-3D':
                                special_tags.append('🥽DualFish-3D')
                            elif vtype == '360°-EQR':
                                special_tags.append('🌐360°-EQR')
                            elif vtype == '360°':
                                special_tags.append('🌐360°')
                            elif vtype == 'VR':
                                special_tags.append('🌐VR')
                            elif vtype == '3D':
                                special_tags.append('🥽3D')
                            elif vtype == '180°':
                                special_tags.append('📹180°VR')
                            elif vtype == 'HDR':
                                special_tags.append('✨HDR')
                            else:
                                special_tags.append(f'🎯{vtype}')
                    
                    special_display = ' '.join(special_tags)
                    if special_display:
                        special_display = f" {special_display}"
                    
                    fps = f" @{fmt['fps']}fps" if fmt.get('fps') else ""
                    size = self.format_filesize(fmt.get('filesize'))
                    vcodec = fmt.get('vcodec', 'unknown')[:12]
                    
                    # Show if it's video+audio or video-only
                    format_type = ""
                    if fmt['type'] == 'video+audio':
                        acodec = fmt.get('acodec', 'unknown')[:8]
                        format_type = f" (V:{vcodec}/A:{acodec})"
                    else:
                        format_type = f" (V:{vcodec}/Video Only)"
                    
                    # Add format notes for additional info
                    note = fmt.get('format_note', '')
                    if note and len(note) < 30:
                        format_type += f" [{note}]"
                    
                    print(f"{option_num}. 🎬 {fmt['ext'].upper()} - {res_display}{fps}{special_display}{format_type} [{size}]")
                    option_num += 1
        
        print(f"\n0. ❌ Cancel and enter new URL")
        print("-" * 70)
        
        return options
    
    def get_user_choice(self, max_options):
        """Get user's download choice"""
        while True:
            try:
                choice = input(f"\n🎯 Enter your choice (0-{max_options}): ").strip()
                
                if not choice:
                    print("⚠️ Please enter a number")
                    continue
                
                choice_num = int(choice)
                
                if choice_num == 0:
                    return 0  # Cancel
                elif 1 <= choice_num <= max_options:
                    return choice_num
                else:
                    print(f"⚠️ Please enter a number between 0 and {max_options}")
                    
            except ValueError:
                print("⚠️ Please enter a valid number")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                sys.exit(0)
    
    def create_download_options(self, selected_option):
        """Create yt-dlp options based on user selection"""
        base_opts = {
            'outtmpl': f'{self.download_dir}/%(title)s.%(ext)s',
            'ignoreerrors': False,
        }
        
        if selected_option['type'] == 'quick_video_mkv':
            base_opts.update({
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mkv',
            })
        elif selected_option['type'] == 'quick_video_mp4':
            base_opts.update({
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
            })
        elif selected_option['type'] == 'vr_video':
            base_opts.update({
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mkv',
                'writeinfojson': True,
            })
        elif selected_option['type'] == '3d_video':
            base_opts.update({
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mkv',
                'writeinfojson': True,
            })
        elif selected_option['type'] == 'quick_audio':
            base_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
            })
        elif selected_option['type'] in ['video', 'video_only']:
            if selected_option['info']['type'] == 'video_only':
                base_opts.update({
                    'format': f"{selected_option['format']}+bestaudio/best",
                    'merge_output_format': 'mkv' if selected_option['ext'] in ['webm', 'mkv'] else 'mp4',
                })
            else:
                base_opts['format'] = selected_option['format']
        else:
            base_opts['format'] = selected_option['format']
        
        return base_opts
    
    def download_video(self, url, options):
        """Download the video with selected options"""
        print(f"\n📁 Download directory: {os.path.abspath(self.download_dir)}")
        
        # Create download directory
        Path(self.download_dir).mkdir(exist_ok=True)
        
        print(f"⬇️ Starting download...")
        print("-" * 50)
        
        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([url])
                
            print("\n✅ Download completed successfully!")
            print(f"📁 Files saved to: {os.path.abspath(self.download_dir)}")
            return True
            
        except yt_dlp.DownloadError as e:
            print(f"\n❌ Download failed: {e}")
            return False
        except KeyboardInterrupt:
            print(f"\n⏹️ Download cancelled by user")
            return False
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            return False
    
    def get_url_from_user(self):
        """Get URL from user with validation"""
        while True:
            try:
                print("\n📎 Enter the video URL (or 'quit' to exit):")
                url = input("🔗 URL: ").strip()
                
                if url.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    sys.exit(0)
                
                if not url:
                    print("⚠️ Please enter a URL")
                    continue
                
                if not self.validate_url(url):
                    print("⚠️ Invalid URL format. Please enter a valid HTTP/HTTPS URL")
                    continue
                
                return url
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                sys.exit(0)
    
    def ask_download_directory(self):
        """Ask user for download directory"""
        print(f"\n📁 Current download directory: {os.path.abspath(self.download_dir)}")
        change = input("📝 Change download directory? (y/N): ").strip().lower()
        
        if change in ['y', 'yes']:
            while True:
                new_dir = input("📂 Enter new directory path (or press Enter for current): ").strip()
                
                if not new_dir:
                    break
                
                try:
                    Path(new_dir).mkdir(parents=True, exist_ok=True)
                    self.download_dir = new_dir
                    print(f"✅ Directory changed to: {os.path.abspath(self.download_dir)}")
                    break
                except Exception as e:
                    print(f"❌ Error creating directory: {e}")
    
    def run(self):
        """Main application loop"""
        self.print_banner()
        
        # Check for FFmpeg
        print("🔧 Checking system requirements...")
        try:
            import subprocess
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            print("✅ FFmpeg is installed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️ Warning: FFmpeg not found. Audio conversion may not work.")
            print("📦 Install FFmpeg:")
            print("   • Windows: choco install ffmpeg")
            print("   • macOS: brew install ffmpeg")
            print("   • Linux: sudo apt install ffmpeg")
        
        while True:
            try:
                # Get URL from user
                url = self.get_url_from_user()
                
                # Ask about download directory
                self.ask_download_directory()
                
                # Fetch video info and formats
                info, video_formats, audio_formats = self.get_video_info(url)
                
                if not info:
                    print("❌ Could not fetch video information. Please check the URL and try again.")
                    continue
                
                # Display video information
                self.display_video_info(info)
                
                # Display format options
                options = self.display_format_options(video_formats, audio_formats, info)
                
                if not options:
                    print("❌ No download formats available for this video.")
                    continue
                
                # Get user choice
                choice = self.get_user_choice(len(options))
                
                if choice == 0:  # Cancel
                    continue
                
                selected_option = options[choice - 1]
                
                # Create download options
                download_opts = self.create_download_options(selected_option)
                
                # Confirm download
                description = selected_option.get('description', f"{selected_option['type']} format")
                print(f"\n📋 You selected: {description}")
                confirm = input("✅ Proceed with download? (Y/n): ").strip().lower()
                
                if confirm in ['', 'y', 'yes']:
                    # Start download
                    success = self.download_video(url, download_opts)
                    
                    if success:
                        # Ask if user wants to download another video
                        again = input("\n🔄 Download another video? (Y/n): ").strip().lower()
                        if again in ['n', 'no']:
                            print("👋 Thank you for using YouDownloader!")
                            break
                    else:
                        print("💡 You can try a different format or check your internet connection.")
                else:
                    print("❌ Download cancelled.")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                print("🔄 Restarting...")

def main():
    """Entry point"""
    try:
        downloader = YouDownloader()
        downloader.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()