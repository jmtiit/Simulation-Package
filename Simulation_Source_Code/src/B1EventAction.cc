//
// ********************************************************************
// * License and Disclaimer                                           *
// *                                                                  *
// * The  Geant4 software  is  copyright of the Copyright Holders  of *
// * the Geant4 Collaboration.  It is provided  under  the terms  and *
// * conditions of the Geant4 Software License,  included in the file *
// * LICENSE and available at  http://cern.ch/geant4/license .  These *
// * include a list of copyright holders.                             *
// *                                                                  *
// * Neither the authors of this software system, nor their employing *
// * institutes,nor the agencies providing financial support for this *
// * work  make  any representation or  warranty, express or implied, *
// * regarding  this  software system or assume any liability for its *
// * use.  Please see the license in the file  LICENSE  and URL above *
// * for the full disclaimer and the limitation of liability.         *
// *                                                                  *
// * This  code  implementation is the result of  the  scientific and *
// * technical work of the GEANT4 collaboration.                      *
// * By using,  copying,  modifying or  distributing the software (or *
// * any work based  on the software)  you  agree  to acknowledge its *
// * use  in  resulting  scientific  publications,  and indicate your *
// * acceptance of all terms of the Geant4 Software license.          *
// ********************************************************************
//
//
/// \file B1EventAction.cc
/// \brief Implementation of the B1EventAction class

#include "B1EventAction.hh"
#include "B1RunAction.hh"

#include "G4Event.hh"
#include "G4RunManager.hh"
#include "B1Analysis.hh"


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B1EventAction::B1EventAction(B1RunAction* runAction)
: G4UserEventAction(),
  fRunAction(runAction),
  fEdep(0.)
{} 

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B1EventAction::~B1EventAction()
{}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void B1EventAction::BeginOfEventAction(const G4Event*)
{    
  fEdep = 0.;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void B1EventAction::EndOfEventAction(const G4Event* event)
{   
  // accumulate statistics in run action
  fRunAction->AddEdep(fEdep);
  
  //
  // Fill ntuple
  //
  //=================================

 
  // Get analysis manager
  //auto analysisManager = G4AnalysisManager::Instance();
 
  // Fill ntuple
 
  //G4PrimaryVertex* primaryVertex = event->GetPrimaryVertex();
  //G4PrimaryParticle* particle = primaryVertex->GetPrimary();

  //G4String particleName = particle->GetParticleDefinition()->GetParticleName();

  //G4double x0 = primaryVertex->GetX0();
  //G4double y0 = primaryVertex->GetY0();
  //G4double z0 = primaryVertex->GetZ0();
  //G4double t0 = primaryVertex->GetT0();
  //G4double k  = particle->GetKineticEnergy();
  //G4double e  = particle->GetTotalEnergy();
  //G4double px = particle->GetPx();
  //G4double py = particle->GetPy();
  //G4double pz = particle->GetPz();
 
  //analysisManager->FillNtupleSColumn(0, particleName);
  //analysisManager->FillNtupleDColumn(1, x0);
  //analysisManager->FillNtupleDColumn(2, y0);
  //analysisManager->FillNtupleDColumn(3, z0);
  //analysisManager->FillNtupleDColumn(4, k);

  //analysisManager->AddNtupleRow();
  
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
