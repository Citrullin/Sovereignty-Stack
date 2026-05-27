const puppeteer = require('puppeteer');
const fs = require('fs');
const { execSync } = require('child_process');

(async () => {
    const email = process.env.PARALUS_EMAIL || 'admin@paralus.local';
    const password = process.env.PARALUS_PASSWORD || 'ParalusAdmin123!';
    const host = process.env.NODE_IP || 'istio-ingress.istio-system.svc.cluster.local';
    const clusterName = process.env.PARALUS_CLUSTER_NAME || 'local-k3s';

    const browser = await puppeteer.launch({
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--ignore-certificate-errors',
            '--disable-dev-shm-usage',
            `--host-rules=MAP paralus.homelab.local ${host}`
        ],
        headless: 'new',
        protocolTimeout: 60000
    });

    try {
        const page = await browser.newPage();

        console.log(`[1/4] Logging in as ${email}...`);
        await page.goto('https://paralus.homelab.local/', { waitUntil: 'networkidle2' });

        await page.waitForSelector('input#email', { timeout: 10000 });
        await page.type('input#email', email);
        await page.type('input#password', password);

        await Promise.all([
            page.waitForNavigation({ waitUntil: 'networkidle2' }),
            page.evaluate(() => {
                const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Login'));
                if (btn) btn.click();
            })
        ]);
        console.log('[1/4] Login successful.');

        console.log(`[2/4] Registering new cluster "${clusterName}"...`);

        const clusterData = {
            kind: "Cluster",
            metadata: {
                name: clusterName,
                description: "Local K3s homelab cluster deployed via automated job"
            },
            spec: {
                clusterType: "imported",
                params: {
                    provisionType: "IMPORT",
                    provisionEnvironment: "ONPREM",
                    provisionPackageType: "",
                    environmentProvider: "",
                    kubernetesProvider: "OTHER",
                    state: "CONFIG"
                }
            }
        };

        const result = await page.evaluate(async (payload) => {
            const res = await fetch('/infra/v3/project/default/cluster', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            const text = await res.text();
            return { status: res.status, body: text };
        }, clusterData);

        if (result.status >= 400 && !(result.status === 500 && result.body.includes('already taken'))) {
            throw new Error(`Cluster registration failed: ${result.status} - ${result.body}`);
        }

        console.log(`[2/4] Cluster "${clusterName}" registered.`);

        console.log('[3/4] Downloading Bootstrap YAML...');
        const bootstrapResult = await page.evaluate(async (name) => {
            const res = await fetch(`/infra/v3/project/default/cluster/${name}/download`, {
                headers: { 'Accept': 'application/json' }
            });
            return { status: res.status, body: await res.text() };
        }, clusterName);

        if (bootstrapResult.status === 200) {
            console.log("Bootstrap YAML downloaded to /tmp/paralus-bootstrap.yaml.");
            let actualYaml = bootstrapResult.body;
            try {
                const parsed = JSON.parse(bootstrapResult.body);
                if (parsed.data) {
                    actualYaml = Buffer.from(parsed.data, 'base64').toString('utf-8');
                }
            } catch (e) { }
            // Inject insecure bootstrap flag so the Relay Agent doesn't crash TLS verification
            actualYaml = actualYaml.replace(
                "templateName:",
                "allowInsecureBootstrap: \"true\"\n  templateName:"
            );
            fs.writeFileSync('/tmp/paralus-bootstrap.yaml', actualYaml);
        } else {
            throw new Error(`Failed to download bootstrap YAML: ${bootstrapResult.status}`);
        }

        console.log('[4/4] Applying Bootstrap YAML inside cluster...');

        // Download kubectl because the puppeteer image doesn't have it
        console.log('Downloading kubectl...');
        execSync('curl -sLO "https://dl.k8s.io/release/v1.28.4/bin/linux/amd64/kubectl" && chmod +x kubectl');

        // Apply the bootstrap YAML
        // We assume this pod is running with a ServiceAccount that has cluster-admin privileges
        console.log('Applying YAML...');
        const applyOutput = execSync('./kubectl apply -f /tmp/paralus-bootstrap.yaml').toString();
        console.log(applyOutput);

        console.log('--- ALL TASKS COMPLETE ---');

    } catch (e) {
        console.error('Error during cluster registration:', e);
        process.exit(1);
    } finally {
        await browser.close();
    }
})();
