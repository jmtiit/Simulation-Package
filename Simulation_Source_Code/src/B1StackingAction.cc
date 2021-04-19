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
/// \file OpNovice/src/OpNoviceStackingAction.cc
/// \brief Implementation of the OpNoviceStackingAction class
//
//
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#include "B1StackingAction.hh"
#include "B1RunAction.hh"
#include "B1Analysis.hh"

#include "G4VProcess.hh"

#include "G4ParticleDefinition.hh"
#include "G4ParticleTypes.hh"
#include "G4Track.hh"
#include "G4ios.hh"

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B1StackingAction::B1StackingAction()
  : G4UserStackingAction(),
    feCounter(0), fgammaCounter(0), fpiCounter(0), fKCounter(0), fprotonCounter(0), fneutronCounter(0), feEnergySum(0), fgammaEnergySum(0), fpiEnergySum(0), fprotonEnergySum(0), fneutronEnergySum(0)
{}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B1StackingAction::~B1StackingAction()
{}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

G4ClassificationOfNewTrack
B1StackingAction::ClassifyNewTrack(const G4Track * aTrack)
{

  G4cout << "PDGEncoding: " << aTrack->GetDefinition()->GetPDGEncoding() << G4endl;
	
  switch(aTrack->GetDefinition()->GetPDGEncoding())
  {
    case -11 : //positron
    case 11 : //electron
      ++feCounter;
      feEnergySum+=aTrack->GetKineticEnergy();
      break;
    case 22 : //gamma
      ++fgammaCounter;
      fgammaEnergySum+=aTrack->GetKineticEnergy();
      break;
    case 211 : //pi+
    case -211: //pi-
    case 111 : //pi0
      ++fpiCounter;
      fpiEnergySum+=aTrack->GetKineticEnergy();
      break;
    case 321 : //kaon+
    case -321 : //kaon-
      ++fKCounter;
      break;
    case 2212 : //proton
      ++fprotonCounter;
      fprotonEnergySum+=aTrack->GetKineticEnergy();
      break;
    case 2112 : //neutron
      ++fneutronCounter;
      fneutronEnergySum+=aTrack->GetKineticEnergy();
      break;
  }

  G4cout << "feCounter: " << feCounter << G4endl;
  G4cout << "fgammaCounter: " << fgammaCounter << G4endl;
  G4cout << "fpiCounter: " << fpiCounter << G4endl;
  G4cout << "fKCounter: " << fKCounter << G4endl;
  G4cout << "fprotonCounter: " << fprotonCounter << G4endl;
  G4cout << "fneutronCounter: " << fneutronCounter << G4endl;  
 
 
  return fUrgent;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void B1StackingAction::NewStage()
{
  //  G4cout << "Number of Scintillation photons produced in this event : "
  //         << fScintillationCounter << G4endl;
  // G4cout << "Number of Cerenkov photons produced in this event : "
  //     << fCerenkovCounter << G4endl;

  G4double feAvgEnergy=(feCounter>0)? feEnergySum/feCounter: 0. ;
  G4double fgammaAvgEnergy=(fgammaCounter>0)? fgammaEnergySum/fgammaCounter: 0. ;
  G4double fpiAvgEnergy=(fpiCounter>0)? fpiEnergySum/fpiCounter: 0. ;
  G4double fprotonAvgEnergy=(fprotonCounter>0)? fprotonEnergySum/fprotonCounter: 0. ;
  G4double fneutronAvgEnergy=(fneutronCounter>0)? fneutronEnergySum/fneutronCounter: 0. ;

 auto analysisManager = G4AnalysisManager::Instance();
 
  // Fill ntuple
 
  analysisManager->FillNtupleIColumn(0, feCounter);
  analysisManager->FillNtupleIColumn(1, fgammaCounter);
  analysisManager->FillNtupleIColumn(2, fpiCounter);
  analysisManager->FillNtupleIColumn(3, fKCounter);
  analysisManager->FillNtupleIColumn(4, fprotonCounter);
  analysisManager->FillNtupleIColumn(5, fneutronCounter);
  analysisManager->FillNtupleDColumn(6, feAvgEnergy);
  analysisManager->FillNtupleDColumn(7, fgammaAvgEnergy);
  analysisManager->FillNtupleDColumn(8, fpiAvgEnergy);
  analysisManager->FillNtupleDColumn(9, fprotonAvgEnergy);
  analysisManager->FillNtupleDColumn(10, fneutronAvgEnergy);

  analysisManager->AddNtupleRow();
  
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void B1StackingAction::PrepareNewEvent()
{
  feCounter = 0;
  fgammaCounter = 0;
  fpiCounter = 0;
  fKCounter = 0;
  fprotonCounter = 0;
  fneutronCounter = 0;
  feEnergySum = 0.;
  fgammaEnergySum = 0.;
  fpiEnergySum = 0.;
  fprotonEnergySum = 0.;
  fneutronEnergySum = 0.;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
