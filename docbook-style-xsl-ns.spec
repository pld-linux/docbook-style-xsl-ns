Summary:	DocBook XSL NS (namespaced) Stylesheets
Summary(pl.UTF-8):	Arkusze stylów XSL NS (z przestrzeniami nazw) dla DocBooka
Name:		docbook-style-xsl-ns
Version:	1.79.0
Release:	2
License:	(C) 1997, 1998 Norman Walsh (Free)
Group:		Applications/Publishing/XML
Source0:	http://downloads.sourceforge.net/docbook/docbook-xsl-ns-%{version}.tar.bz2
# Source0-md5:	bd8220801f87d62053940501ffe9ea80
URL:		http://docbook.sourceforge.net/projects/xsl/index.html
BuildRequires:	libxml2-progs
BuildRequires:	unzip
AutoReqProv:	no
Requires(post,postun):	/etc/xml/catalog
Requires(post,postun):	/usr/bin/xmlcatalog
# workaround for rpm/poldek
Requires:	/etc/xml/catalog
Requires:	libxml2-progs
Requires:	sgml-common >= 0.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		xsl_path	%{_datadir}/sgml/docbook/xsl-ns-stylesheets
%define		catalog		%{xsl_path}/catalog.xml

%description
This package contains a release of XSL stylesheets for processing
namespaced DocBook documents (DocBook 5 or later). The stylesheets are
the same as the concurrent stylesheet release except that the
templates match on elements in the DocBook namespace.

%description -l pl.UTF-8
Ten pakiet zawiera wydanie arkuszy stylów XSL do przetwarzania
dokuemntów DocBooka z przestrzeniami nazw (DocBook 5 lub późniejszy).
Arkusze są takie same jak zwykłe wydanie z tą różnicą, że szablony są
dopasowywane po elementach w przestrzeni nazw DocBooka.

%prep
%setup -q -n docbook-xsl-ns-%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{xsl_path}

cp -a $(find . -mindepth 1 -maxdepth 1 -type d -a ! -name extensions) $RPM_BUILD_ROOT%{xsl_path}
cp -p VERSION.xsl $RPM_BUILD_ROOT%{xsl_path}

%xmlcat_create $RPM_BUILD_ROOT%{catalog}

%xmlcat_add_rewrite http://docbook.sourceforge.net/release/xsl-ns/%{version} file://%{xsl_path} $RPM_BUILD_ROOT%{catalog}
%xmlcat_add_rewrite http://docbook.sourceforge.net/release/xsl-ns/current file://%{xsl_path} $RPM_BUILD_ROOT%{catalog}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if ! grep -q %{catalog} %{_sysconfdir}/xml/catalog ; then
	%xmlcat_add %{catalog}
fi

%preun
if [ "$1" = "0" ] ; then
	%xmlcat_del %{catalog}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS COPYING NEWS README RELEASE-NOTES.{html,txt} TODO
%{xsl_path}
