#
# spec file for package spotify
#
# Copyright (c) 2012 Marguerite Su, Adam Spiers
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

Name:           spotify-client
Version:        1.0.45.186.g3b5036d6
License:        Commercial
Release:        95
Summary:        Desktop client for Spotify streaming music service
Url:            http://www.spotify.com/download/previews/
Group:          Productivity/Multimedia/Sound/Players
%ifarch x86_64
Source0: spotify-client_%{version}-%{release}_amd64.deb
%else
Source0: spotify-client_%{version}-28_i386.deb
%endif
NoSource:       0
%if 0%{?suse_version}
Requires:       mozilla-nss
Requires:       mozilla-nspr
Requires:       libopenssl1_0_0
Requires:       libpng12-0
Recommends:     libmp3lame0
Recommends:     ffmpeg
%endif

# not currently tested on Fedora or Mandriva, but leaving
# these here in case anyone wants to step up and do it :)
%if 0%{?fedora_version}
Requires:       nss
Requires:       nspr
Requires:       openssl >= 1.0.0
%endif
%if 0%{?mandriva_version}
Requires:       libnss3
Requires:       libnspr4
Requires:       libopenssl1.0.0
Conflicts:      libopenssl0.9.8
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Spotify is a "Freemium" proprietary, DRM-restricted digital music
service that gives you access to millions of songs.

It includes the following features:

- Custom playlists
- Last.fm integration
- Customized radio dynamically generated to the user's tastes
- Social media integration with Facebook and Twitter
- 3rd-party applications integrated into the client

%prep
%setup -T -c %{name}_%{version}
# unpack deb
ar -x %{SOURCE0}
# unpack data
tar -xf data.tar.gz
# remove used files
rm data.tar.gz control.tar.gz debian-binary

%define _use_internal_dependency_generator 0
%define __find_requires %_builddir/%{name}-%{version}/find-requires.sh
cat >%__find_requires <<'EOF'
#!/bin/sh
EOF
chmod +x %__find_requires

%build
# no need to build

%install
mv usr %{buildroot}
%define spotifydir /usr/share/spotify
%define desktopdir /usr/share/applications
%define icondir    /usr/share/icons/hicolor

desktop=%{buildroot}%{desktopdir}/spotify.desktop

# for size in ls "%{buildroot}%{spotifydir}/icons/spotify-linux*" | grep -Eo '[0-9]+' ; do
#     mkdir -p %{buildroot}%{icondir}/${size}x${size}/apps/
#     cp %{buildroot}%{spotifydir}/icons/spotify-linux-${size}.png %{buildroot}%{icondir}/${size}x${size}/apps/%{name}.png
# done


mkdir -p %{buildroot}%{desktopdir}
mv %{buildroot}%{spotifydir}/spotify.desktop $desktop
%suse_update_desktop_file $desktop

mkdir -p %{buildroot}%{_docdir}/%{name}
mv %{buildroot}%{_docdir}/../%{name}/* %{buildroot}%{_docdir}/%{name}/
cat >%{buildroot}%{_docdir}/%{name}/README <<EOF
This package was built by the openSUSE Spotify installer; see

    https://github.com/janwillhaus/opensuse-spotify-installer

for more information.
EOF

%post
/sbin/ldconfig
%desktop_database_post
%icon_theme_cache_post


%preun
# nothing to do here.

%postun
if [ "$1" = 0 ]; then
    /sbin/ldconfig
fi
%desktop_database_postun
%icon_theme_cache_postun

%files
%defattr(-,root,root)
%spotifydir
%doc %{_docdir}/%{name}
%{_bindir}/spotify
%{desktopdir}/spotify.desktop

%changelog
* Sat Jan 05 2013 Adam Spiers <spotify-on-opensuse@adamspiers.org>
- add README

* Sat Jan 05 2013 Adam Spiers <spotify-on-opensuse@adamspiers.org>
- update to 0.8.8 (moved to /opt)
- rename to spotify-client for consistency with original Debian package
- use provided register.sh and unregister.sh
- remove need to conflict with libopenssl0_9_8
- fix automatically generated dependencies
- fix XDG categories
- move dedicated library directory to /opt/spotify/spotify-client/lib
- remove spotify-linux-512x512.png since redistribution probably
  violates Spotify copyright
- fix SPOTIFY_CLEAN_CACHE test
- fix passing of multiple arguments to spotify binary

* Mon Aug 20 2012 Marguerite Su <i@marguerite.su> - 0.8.4.103.g9cb117b.260
- initial version with Spotify App support.
- use libopenssl1_0_0 instead of libopenssl0_9_8 to fix a crash and other linkings ready.
- use wrapper to clear cache manually
