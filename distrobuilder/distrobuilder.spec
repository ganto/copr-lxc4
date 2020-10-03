%if 0%{?fedora}
%global with_devel 1
%global with_debug 1
%global with_check 1
%global with_unit_test 1
%else
%global with_devel 1
%global with_debug 1
%global with_check 1
%global with_unit_test 1
%endif

%if 0%{?with_debug}
%global _find_debuginfo_dwz_opts %{nil}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%if 0%{?centos} == 8
# fails to find the source files
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif
%else
%global debug_package   %{nil}
%endif

%if 0%{?centos}
# centos doesn't (yet) define build macros for golang
%define gobuild(o:) %{expand:
  go build -buildmode pie -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '%__global_ldflags %{?__golang_extldflags}'" -a -v -x %{?**};
}
# Define commands for testing
%define gotestflags      -buildmode pie -compiler gc
%define gotestextldflags %__global_ldflags %{?__golang_extldflags}
%define gotest() go test %{gotestflags} -ldflags "${LDFLAGS:-} -extldflags '%{gotestextldflags}'" %{?**};
%endif

%global provider        github
%global provider_tld    com
%global project         lxc
%global repo            distrobuilder
# https://github.com/lxc/distrobuilder
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}

Name:       %{repo}
Version:    1.0
Release:    0.1%{?dist}
Summary:    System container image builder for LXC and LXD

License:    ASL 2.0
URL:        https://%{provider_prefix}
Source0:    https://linuxcontainers.org/downloads/distrobuilder/%{name}-%{version}.tar.gz
Patch0:     %{repo}-%{version}-Disable-online-tests.patch

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

BuildRequires:  help2man

Requires:       gnupg
Requires:       squashfs-tools
Requires:       tar

%description
%{summary}.

%if 0%{?with_devel}
%package devel
Summary:        System container image builder - Source Libraries
BuildArch:      noarch

%if 0%{?with_check}
BuildRequires:  gnupg
BuildRequires:  squashfs-tools
%endif

# Avoid duplicated Provides of bundled libraries
Autoprov:       0
Provides:       %{name}-devel = %{version}-%{release}

Provides:       golang(%{import_path}/generators) = %{version}-%{release}
Provides:       golang(%{import_path}/image) = %{version}-%{release}
Provides:       golang(%{import_path}/managers) = %{version}-%{release}
Provides:       golang(%{import_path}/shared) = %{version}-%{release}
Provides:       golang(%{import_path}/sources) = %{version}-%{release}

# generated from _dist/MANIFEST
Provides:       bundled(golang(github.com/antchfx/xpath)) = 668f6670d6ae1409249cc09be7907702e7f8152f
Provides:       bundled(golang(github.com/flosch/pongo2)) = bbf5a6c351f4d4e883daa40046a404d7553e0a00
Provides:       bundled(golang(github.com/gobuffalo/envy)) = 909ea676d4c90832fefbf55a5a4fb04d8bef8931
Provides:       bundled(golang(github.com/gobuffalo/logger)) = 7c291b53e05b81d77bd43109b4a3c6f84e45c8e1
Provides:       bundled(golang(github.com/gobuffalo/packd)) = 54ea459691466cfb630ccc276723fe3963f3e9d5
Provides:       bundled(golang(github.com/gobuffalo/packr)) = 4b4a3c432a2e5a17b4f14c971179b40021c67530
Provides:       bundled(golang(github.com/gobuffalo/packr/builder)) = 4b4a3c432a2e5a17b4f14c971179b40021c67530
Provides:       bundled(golang(github.com/gobuffalo/packr/packr)) = 4b4a3c432a2e5a17b4f14c971179b40021c67530
Provides:       bundled(golang(github.com/gobuffalo/packr/v2)) = 4b4a3c432a2e5a17b4f14c971179b40021c67530
Provides:       bundled(golang(github.com/gobuffalo/packr/v2/file)) = 4b4a3c432a2e5a17b4f14c971179b40021c67530
Provides:       bundled(golang(github.com/gobuffalo/packr/v2/file/resolver)) = 4b4a3c432a2e5a17b4f14c971179b40021c67530
Provides:       bundled(golang(github.com/gobuffalo/packr/v2/file/resolver/encoding/hex)) = 4b4a3c432a2e5a17b4f14c971179b40021c67530
Provides:       bundled(golang(github.com/gobuffalo/packr/v2/jam)) = 4b4a3c432a2e5a17b4f14c971179b40021c67530
Provides:       bundled(golang(github.com/gobuffalo/packr/v2/jam/parser)) = 4b4a3c432a2e5a17b4f14c971179b40021c67530
Provides:       bundled(golang(github.com/gobuffalo/packr/v2/jam/store)) = 4b4a3c432a2e5a17b4f14c971179b40021c67530
Provides:       bundled(golang(github.com/gobuffalo/packr/v2/packr2)) = 4b4a3c432a2e5a17b4f14c971179b40021c67530
Provides:       bundled(golang(github.com/gobuffalo/packr/v2/plog)) = 4b4a3c432a2e5a17b4f14c971179b40021c67530
Provides:       bundled(golang(github.com/gorilla/websocket)) = c3e18be99d19e6b3e8f1559eea2c161a665c4b6b
Provides:       bundled(golang(github.com/joho/godotenv)) = b09de681dcaff3eaeafcc62ee1f9f622a0c32b8b
Provides:       bundled(golang(github.com/joho/godotenv/autoload)) = b09de681dcaff3eaeafcc62ee1f9f622a0c32b8b
Provides:       bundled(golang(github.com/juju/errors)) = d42613fe1ab9e303fc850e7a19fda2e8eeb6516e
Provides:       bundled(golang(github.com/lxc/lxd/client)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/fuidshift)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxc)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxc/config)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxc-to-lxd)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxc/utils)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/apparmor)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/backup)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd-benchmark)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd-benchmark/benchmark)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/cgroup)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/cluster)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/cluster/raft)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/config)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/daemon)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/db)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/db/cluster)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/db/node)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/db/query)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/db/schema)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/device)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/device/config)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/dnsmasq)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/endpoints)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/events)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/instance/instancetype)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/instance/operationlock)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/iptables)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/maas)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/migration)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/node)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/operations)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd-p2c)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/project)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/rbac)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/resources)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/response)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/rsync)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/seccomp)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/state)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/storage)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/storage/quota)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/sys)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/task)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/template)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/ucred)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/lxd/util)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/api)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/cancel)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/containerwriter)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/dnsutil)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/eagain)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/generate)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/generate/db)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/generate/file)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/generate/lex)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/i18n)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/idmap)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/ioprogress)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/log15)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/log15/stack)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/log15/term)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/logger)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/logging)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/netutils)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/osarch)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/simplestreams)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/subtest)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/termios)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/units)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/lxc/lxd/shared/version)) = 08eccb1b52fece5c3008a7a2b412771359ad0a86
Provides:       bundled(golang(github.com/mudler/docker-companion)) = 6a693e9b9eaf2cd08ba628350613f2e08e9af57d
Provides:       bundled(golang(github.com/mudler/docker-companion/api)) = 6a693e9b9eaf2cd08ba628350613f2e08e9af57d
Provides:       bundled(golang(github.com/pkg/errors)) = 27936f6d90f9c8e1145f11ed52ffffbfdb9e0af7
Provides:       bundled(golang(github.com/rogpeppe/go-internal/cache)) = d89504fbbf2c313df24867a5ffafcc9b847961ff
Provides:       bundled(golang(github.com/rogpeppe/go-internal/dirhash)) = d89504fbbf2c313df24867a5ffafcc9b847961ff
Provides:       bundled(golang(github.com/rogpeppe/go-internal/fmtsort)) = d89504fbbf2c313df24867a5ffafcc9b847961ff
Provides:       bundled(golang(github.com/rogpeppe/go-internal/goproxytest)) = d89504fbbf2c313df24867a5ffafcc9b847961ff
Provides:       bundled(golang(github.com/rogpeppe/go-internal/gotooltest)) = d89504fbbf2c313df24867a5ffafcc9b847961ff
Provides:       bundled(golang(github.com/rogpeppe/go-internal/imports)) = d89504fbbf2c313df24867a5ffafcc9b847961ff
Provides:       bundled(golang(github.com/rogpeppe/go-internal/lockedfile)) = d89504fbbf2c313df24867a5ffafcc9b847961ff
Provides:       bundled(golang(github.com/rogpeppe/go-internal/modfile)) = d89504fbbf2c313df24867a5ffafcc9b847961ff
Provides:       bundled(golang(github.com/rogpeppe/go-internal/module)) = d89504fbbf2c313df24867a5ffafcc9b847961ff
Provides:       bundled(golang(github.com/rogpeppe/go-internal/par)) = d89504fbbf2c313df24867a5ffafcc9b847961ff
Provides:       bundled(golang(github.com/rogpeppe/go-internal/renameio)) = d89504fbbf2c313df24867a5ffafcc9b847961ff
Provides:       bundled(golang(github.com/rogpeppe/go-internal/semver)) = d89504fbbf2c313df24867a5ffafcc9b847961ff
Provides:       bundled(golang(github.com/rogpeppe/go-internal/testenv)) = d89504fbbf2c313df24867a5ffafcc9b847961ff
Provides:       bundled(golang(github.com/rogpeppe/go-internal/testscript)) = d89504fbbf2c313df24867a5ffafcc9b847961ff
Provides:       bundled(golang(github.com/rogpeppe/go-internal/txtar)) = d89504fbbf2c313df24867a5ffafcc9b847961ff
Provides:       bundled(golang(github.com/sirupsen/logrus)) = fb62dbe2f2a2c88b150fa1668a773505a7920a3d
Provides:       bundled(golang(github.com/sirupsen/logrus/hooks/syslog)) = fb62dbe2f2a2c88b150fa1668a773505a7920a3d
Provides:       bundled(golang(github.com/spf13/cobra)) = 77e4d5aecc4d34e58f72e5a1c4a5a13ef55e6f44
Provides:       bundled(golang(github.com/spf13/cobra/cobra)) = 77e4d5aecc4d34e58f72e5a1c4a5a13ef55e6f44
Provides:       bundled(golang(github.com/spf13/cobra/cobra/tpl)) = 77e4d5aecc4d34e58f72e5a1c4a5a13ef55e6f44
Provides:       bundled(golang(github.com/spf13/cobra/doc)) = 77e4d5aecc4d34e58f72e5a1c4a5a13ef55e6f44
Provides:       bundled(golang(github.com/spf13/pflag)) = 2e9d26c8c37aae03e3f9d4e90b7116f5accb7cab
Provides:       bundled(golang(github.com/stretchr/testify)) = 85f2b59c4459e5bf57488796be8c3667cb8246d6
Provides:       bundled(golang(github.com/stretchr/testify/assert)) = 85f2b59c4459e5bf57488796be8c3667cb8246d6
Provides:       bundled(golang(github.com/stretchr/testify/http)) = 85f2b59c4459e5bf57488796be8c3667cb8246d6
Provides:       bundled(golang(github.com/stretchr/testify/mock)) = 85f2b59c4459e5bf57488796be8c3667cb8246d6
Provides:       bundled(golang(github.com/stretchr/testify/require)) = 85f2b59c4459e5bf57488796be8c3667cb8246d6
Provides:       bundled(golang(github.com/stretchr/testify/suite)) = 85f2b59c4459e5bf57488796be8c3667cb8246d6
Provides:       bundled(golang(golang.org/x/crypto/acme)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/acme/autocert)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/argon2)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/bcrypt)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/blake2b)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/blake2s)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/blowfish)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/bn256)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/cast5)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/chacha20poly1305)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/cryptobyte)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/cryptobyte/asn1)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/curve25519)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/ed25519)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/hkdf)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/md4)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/nacl/auth)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/nacl/box)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/nacl/secretbox)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/nacl/sign)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/ocsp)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/openpgp)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/openpgp/armor)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/openpgp/clearsign)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/openpgp/elgamal)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/openpgp/errors)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/openpgp/packet)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/openpgp/s2k)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/otr)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/pbkdf2)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/pkcs12)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/poly1305)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/ripemd160)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/salsa20)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/salsa20/salsa)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/scrypt)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/sha3)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/ssh)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/ssh/agent)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/ssh/knownhosts)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/ssh/terminal)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/tea)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/twofish)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/xtea)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/crypto/xts)) = 87dc89f01550277dc22b74ffcf4cd89fa2f40f4c
Provides:       bundled(golang(golang.org/x/net/bpf)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/context)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/context/ctxhttp)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/dict)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/dns/dnsmessage)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/html)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/html/atom)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/html/charset)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/http2)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/http2/h2c)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/http2/h2demo)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/http2/h2i)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/http2/hpack)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/http/httpguts)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/http/httpproxy)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/icmp)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/idna)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/ipv4)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/ipv6)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/lif)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/nettest)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/netutil)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/proxy)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/publicsuffix)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/route)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/trace)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/webdav)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/websocket)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/net/xsrftoken)) = ec77196f6094c3492a8b61f2c11cf937f78992ae
Provides:       bundled(golang(golang.org/x/sys/cpu)) = 3e7259c5e7c2076bb2728047a3df75adb1bad8e5
Provides:       bundled(golang(golang.org/x/sys/plan9)) = 3e7259c5e7c2076bb2728047a3df75adb1bad8e5
Provides:       bundled(golang(golang.org/x/sys/unix)) = 3e7259c5e7c2076bb2728047a3df75adb1bad8e5
Provides:       bundled(golang(golang.org/x/sys/unix/linux)) = 3e7259c5e7c2076bb2728047a3df75adb1bad8e5
Provides:       bundled(golang(golang.org/x/sys/windows)) = 3e7259c5e7c2076bb2728047a3df75adb1bad8e5
Provides:       bundled(golang(golang.org/x/sys/windows/mkwinsyscall)) = 3e7259c5e7c2076bb2728047a3df75adb1bad8e5
Provides:       bundled(golang(golang.org/x/sys/windows/registry)) = 3e7259c5e7c2076bb2728047a3df75adb1bad8e5
Provides:       bundled(golang(golang.org/x/sys/windows/svc)) = 3e7259c5e7c2076bb2728047a3df75adb1bad8e5
Provides:       bundled(golang(golang.org/x/sys/windows/svc/debug)) = 3e7259c5e7c2076bb2728047a3df75adb1bad8e5
Provides:       bundled(golang(golang.org/x/sys/windows/svc/eventlog)) = 3e7259c5e7c2076bb2728047a3df75adb1bad8e5
Provides:       bundled(golang(golang.org/x/sys/windows/svc/mgr)) = 3e7259c5e7c2076bb2728047a3df75adb1bad8e5
Provides:       bundled(golang(golang.org/x/text)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/cases)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/collate)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/collate/build)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/collate/tools/colcmp)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/currency)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/date)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/encoding)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/encoding/charmap)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/encoding/htmlindex)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/encoding/ianaindex)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/encoding/japanese)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/encoding/korean)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/encoding/simplifiedchinese)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/encoding/traditionalchinese)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/encoding/unicode)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/encoding/unicode/utf32)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/feature/plural)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/language)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/language/display)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/message)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/message/catalog)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/message/pipeline)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/number)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/runes)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/search)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/secure)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/secure/bidirule)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/secure/precis)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/transform)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/unicode)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/unicode/bidi)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/unicode/cldr)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/unicode/norm)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/unicode/rangetable)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/unicode/runenames)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(golang.org/x/text/width)) = 3d0f7978add91030e5e8976ff65ccdd828286cba
Provides:       bundled(golang(gopkg.in/antchfx/htmlquery.v1)) = 1d2a462a405c81a14855323a686036cf229f7fe6
Provides:       bundled(golang(gopkg.in/flosch/pongo2.v3)) = 5e81b817a0c48c1c57cdf1a9056cf76bdee02ca9
Provides:       bundled(golang(gopkg.in/robfig/cron.v2)) = be2e0b0deed5a68ffee390b4583a13aff8321535
Provides:       bundled(golang(gopkg.in/yaml.v2)) = f221b8435cfb71e54062f6c6e99e9ade30b124d5

%description devel
%{summary}.

This package contains library sources intended for building other packages
which use the import path %{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test-devel
Summary:        Unit tests for %{name} package
BuildArch:      noarch
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

# test subpackage tests code from devel subpackage
Requires:       %{name}-devel = %{version}-%{release}

Requires:       gnupg
Requires:       squashfs-tools

%description unit-test-devel
%{summary}.

This package contains unit tests for project providing packages with
%{import_path} prefix.
%endif

%prep
%autosetup -n %{name}-%{version} -p1

# move content of vendor under Godeps as has been so far
mkdir -p Godeps/_workspace/src
mv _dist/src/* Godeps/_workspace/src/.

%build
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../ src/%{import_path}

export GOPATH=$(pwd):$(pwd)/Godeps/_workspace:%{gopath}

%gobuild -o _bin/%{name} %{import_path}/%{name}

help2man _bin/%{name} -n "System container image builder" --no-info --no-discard-stderr > %{name}.1

%install
install -d %{buildroot}%{_bindir}
install -p -m 0755 _bin/%{name} %{buildroot}%{_bindir}/%{name}

install -d -m 0755 %{buildroot}%{_mandir}/man1
cp -p %{name}.1 %{buildroot}%{_mandir}/man1

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go"); do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test.file-list
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
export GOPATH=%{buildroot}/%{gopath}:$(pwd)/Godeps/_workspace:%{gopath}

%gotest %{import_path}/image
%gotest %{import_path}/generators
%gotest %{import_path}/shared

%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license COPYING
%doc doc/*.md
%doc doc/examples
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz

%if 0%{?with_devel}
%files devel -f devel.file-list
%license COPYING
%endif

%if 0%{?with_unit_test}
%files unit-test-devel -f unit-test.file-list
%license COPYING
%endif

%changelog
* Thu Oct 24 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.0-0.1
- Update to 1.0
- Add man-page through help2man

* Wed Jul 10 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0-0.1.20190710gitd686c88
- Update to commit d686c88 from July 10, 2019

* Sat Sep 22 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0-0.1.20180707git7274ea2
- Update to commit 7274ea2 from Jul 7, 2018

* Fri Jun 01 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0-0.1.20180522gita15b067
- Update to commit a15b067 from May 22, 2018

* Tue May 08 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0-0.1.20180428git406fd5f
- Update to commit 406fd5f from Apr 28, 2018

* Wed Apr 04 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0-0.1.20180403gitc0e1763
- Initial package
