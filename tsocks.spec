#
# Conditional build:
%bcond_with	forcedns	# intercept and force DNS lookups to use TCP
#
Summary:	tsocks - provide transparent SOCKS support
Summary(pl.UTF-8):   tsocks - przezroczyste wsparcie dla SOCKS
Name:		tsocks
Version:	1.8
%define	_beta	beta5
Release:	0.%{_beta}.1
License:	GPL v2
Group:		Networking/Utilities
Source0:	http://ftp1.sourceforge.net/tsocks/%{name}-%{version}%{_beta}.tar.gz
# Source0-md5:	51caefd77e5d440d0bbd6443db4fc0f8
URL:		http://tsocks.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
tsocks provides transparent network access through a SOCKS proxy. This
is common in firewalled LAN environments where all connections to the
Internet need to pass through a SOCKS server on the firewall. tsocks
intercepts the calls applications make to create TCP connections and
determines if they can be directly accessed or need the SOCKS server.
If they need the SOCKS server they connection is negotiated with the
server transparently to the application. This allows existing
applications to use SOCKS without recompilation or modification.
tsocks is a wrapper library for a number of socket networking
functions. Essentially it's the equivalent of the socksified
winsock.dll libraries that are available for Windows.

%description -l pl.UTF-8
tsocsk udostępnia przezroczysty dostęp do sieci przez proxy SOCKS.
Jest to powszechne w znajdujących się za firewallami sieciach LAN,
gdzie wszystkie połączenia z Internetem muszą przejść przez serwer
SOCKS na firewallu. tsocks przechwytuje zapytania, wykonywane przez
aplikacje w celu stworzenia połączenia TCP i określa, czy mogą one
zostać wykonane bezpośrednio, czy potrzebują serwera SOCKS. Jeśli
potrzebują serwera SOCKS, połączenie jest negocjowane z serwerem w
sposób przezroczysty dla aplikacji. Pozwala to istniejącym aplikacjom
na używanie serwera SOCKS bez rekompilacji lub modyfikacji. tsocks
jest biblioteką-wrapperem dla części funkcji sieciowych, operujących
na gniazdach. Generalnie, jest odpowiednikiem biblioteki winsock.dll,
dostępnej dla Windows.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
cp -f /usr/share/automake/config.sub .
%configure \
	%{?with_forcedns:--enable-socksdns}

%{__make} \
	CFLAGS="%{rpmcflags}" \
	LIBS= \
	SAVE=
# empty SAVE= above is a trick: I don't see a point in building
# /usr/bin/saveme; besides, it implies BR: glibc-static

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_examplesdir}/%{name}-%{version}}

%{__make} install \
	SAVE= \
	DESTDIR=$RPM_BUILD_ROOT

touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf
cp *.example $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
gzip -9n $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog FAQ TODO
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(755,root,root) %{_libdir}/*.so.*
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man?/*
%{_examplesdir}/%{name}-%{version}
